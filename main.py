import datetime as dt
import json
import csv
from pathlib import Path
import copy

"""
Welcome to the Cashier Program made by Anant!
It is a software in which a cashier can easily manage the billing process.
The software can automatically match pricing of items and create bills, and store customer transaction data as history data.
It is a simple yet robust program and an implementation of basic software architecture.
"""

class ListOfItems(object):
    base_list={
        "potato":20,
        "tomato":30,
        "carrot":50,
        "banana":80,
        "apple":150,
        "grape":200,
        "orange":100,
        "flour":50,
        "rice":30,
        "mango":150,
        "onion":100,
        "pulses":110,
        "bread":20,
        "milk":100
    }
    working_dir=Path(__file__).resolve().parent
    file_path=working_dir / "menu.csv"
    try:
        with open(file_path,"r",newline=""):
            pass
    except FileNotFoundError:
        with open(file_path, "w", newline="") as menu_file:
            writer = csv.writer(menu_file)
            for i, j in base_list.items():
                writer.writerow([i, j])

    @classmethod
    def get_list(cls)->dict[str,int]:
        #todo: docstring
        try:
            with open(ListOfItems.file_path,"r") as menu_file:
                reader=csv.reader(menu_file)
                menu={}
                for row in reader:
                    menu.update({row[0]:int(row[1])})
            return menu
        except FileNotFoundError:
            with open(ListOfItems.file_path,"w",newline="") as menu_file:
                writer=csv.writer(menu_file)
                for i,j in ListOfItems.base_list.items():
                    writer.writerow([i,j])
            return ListOfItems.base_list
    @classmethod
    def add_item(cls,item: str,price: int)->int:
        """Used for appending the menu list of items saved in a csv file.
        :return: 0 if successfully updated, -1 if item already exists"""
        try:
            with open(ListOfItems.file_path,"r",newline="") as menu_file:
                check=False
                reader=csv.reader(menu_file)
                for i in reader:
                    if process(item) == i[0]:
                        check=True
        except FileNotFoundError:
            check=False
        if check:
            return -1
        with open(ListOfItems.file_path,"a",newline="") as menu_file:
            writer=csv.writer(menu_file)
            writer.writerow([item,price])
        return 0
    @classmethod
    def del_item(cls,item_name: str)-> int:
        """Used for removing existing items from the menu list csv file
        :return: 0 if successfully updated, -1 if item not found in file"""
        name = process(item_name)
        try:
            with open(ListOfItems.file_path,"r",newline="") as menu_file:
                reader=csv.reader(menu_file)
                updated=[]
                removed=False
                for i in reader:
                    if i[0].lower()==name.lower():
                        removed = True
                        continue
                    updated.append(i)
        except FileNotFoundError:
            updated=[]
            removed=False
        with open(ListOfItems.file_path,"w",newline="") as menu_file:
            writer=csv.writer(menu_file)
            writer.writerows(updated)
        if removed:
            return 0
        else:
            return -1
    @classmethod
    def find_item(cls,item):
        try:
            with open(ListOfItems.file_path,"r",newline="") as menu_file:
                reader=csv.reader(menu_file)
                for i in reader:
                    if i[0].lower()==item.lower():
                        return i[1]
        except FileNotFoundError:
            return -1
        return -1
    @classmethod
    def edit_price(cls,item,new_price):
        try:
            with open(ListOfItems.file_path,"r",newline="") as menu_file:
                reader=csv.reader(menu_file)
                updated=[]
                status=False
                for i in reader:
                    if i[0].lower()==item.lower():
                        status=True
                        old_price=int(i[1])
                        updated.append([i[0],new_price])
                    else:
                        updated.append(i)
        except FileNotFoundError:
            status=False
        with open(ListOfItems.file_path,"w",newline="") as menu_file:
            writer=csv.writer(menu_file)
            writer.writerows(updated)
        if status:
            return old_price
        else:
            return -1
    @classmethod
    def reset_list(cls):
        with open(ListOfItems.file_path, "w", newline="") as menu_file:
            writer = csv.writer(menu_file)
            for i, j in ListOfItems.base_list.items():
                writer.writerow([i, j])

class Cashier(object):
    """
    main cashier class which handles the billing process...
    """
    LoI=ListOfItems.get_list()
    def __init__(self,cashier: str ="Unknown",cust: str="Unknown",cust_num: str="NA"):
        """
        Used to initialize a Cashier object
        """
        self.name=cashier
        self.item=""
        self.items={}
        self.amt=0
        self.cust=cust
        self.custNum=cust_num
    @classmethod
    def refresh_LoI(cls):
        Cashier.LoI=ListOfItems.get_list()
    def billing(self,item,qnt=1):
        """
        This is the core billing method which is used to add items to the billing dictionary...
        It adds the name of the item along with rate and quantity to the billing dictionary...
        :return: 0 if billing was done successfully, -1 if item was not found in the billing dictionary
        """
        item=item.lower()
        try:
            rate=Cashier.LoI[item]
        except KeyError:
            self.item=item
            return -1
        if item in self.items.keys():
            self.items[item][0]+=qnt
            return 0
        self.items.update({item:[qnt,rate]})
        return 0
    def rem_item(self,item):
        """
        This is the method which allows the user to remove any item from the billing dictionary...
        :return: 0 if item was successfully removed, -1 if item was not found in the dictionary
        """
        if item not in self.items:
            self.item = item
            return -1
        self.items.pop(item)
        return 0
    def edit_quan(self,item,qnt=1):
        """
        this is the method used to edit the quantity of an item as billed by the cashier...
        :return: 0 if the bill was edited successfully, -1 if item was not found in the billing dictionary...
        """
        try:
            if item not in self.items.keys() and item in Cashier.LoI.keys():
                self.billing(item,qnt)
                return 0
            a=self.items[item]
            a[0]=qnt
            return 0
        except KeyError:
            self.item=item
            return -1
    def total(self):
        total=0
        if not self.items:
            return total
        else:
            for item,data in self.items.items():
                total += int(data[0])*int(data[1])
            return total
    def get_transaction(self):
        """
        this used to create a snapshot of the transaction
        :return: a transaction object
        """
        self.amt=self.total()
        transaction=Transaction(self.name,self.cust,self.custNum,self.items,self.amt)
        return transaction

class Transaction(object):
    """
    This is the class which is used to create snapshots of a bill transaction...
    """
    def __init__(self,cash_name,cust_name,cust_mob,items,total):
        """
        Initializes the transaction object, to create a snapshot of the transaction...
        :param cash_name: name of the cashier
        :param cust_name: name of the customer
        :param cust_mob: mobile number of the customer
        :param items: the list of items that were billed
        :param total: the total monetary amount
        """
        self.cash_name=cash_name
        self.cust_name=cust_name
        self.cust_mob=cust_mob
        self.items=copy.deepcopy(items)
        self.total=total

class RecHandler(object):
    """
    Used to record a transaction into a JSON file for further access
    """
    working_dir=Path(__file__).resolve().parent
    file_path= working_dir / "record.json"
    def __init__(self,trans):
        """
        It is used to initialize a RecHandler object...
        :param trans: a transaction object
        """
        self.transaction={"cash_name":trans.cash_name, "cust_name":trans.cust_name,"cust_mob":trans.cust_mob,"items":trans.items,"total":trans.total}
    def update_rec(self):
        """
        Used to update the record file by adding the current transaction to the record file...
        """
        rec = []
        try:
            with open(RecHandler.file_path,"r") as f:
                rec=json.load(f)
        except FileNotFoundError:
            pass
        now=dt.datetime.now().strftime("%d-%m-%Y %H:%M ")
        self.transaction.update({"date_time_info":now})
        try:
            rec.append(self.transaction)
        except AttributeError:
            rec= [self.transaction]
        with open(RecHandler.file_path,"w") as f:
            json.dump(rec,f)
    @classmethod
    def get_rec(cls):
        """
        Used to retrieve the data from the record file...
        """
        try:
            with open(RecHandler.file_path,"r") as f:
                rec=json.load(f)
        except FileNotFoundError:
            rec = None
        return rec
    @classmethod
    def retrieve_cust(cls,name,mobile):
        """
        Used to retrieve transaction information of a particular customer using their name and mobile number from the billing record file...
        :param name: the name of the customer whose transaction is to be retrieved
        :param mobile: the mobile number of the customer whose transaction is to be retrieved
        """
        data=RecHandler.get_rec()
        if not data:
            return []
        trans=[]
        for i in data:
            if i["cust_name"]==name.lower() and i["cust_mob"]==mobile:
                trans.append(i)
        return trans
    @classmethod
    def del_rec(cls):
        """
        Used to delete the data from the record file...
        """
        with open(RecHandler.file_path,"w") as f:
            json.dump([],f)

class HelpHandler(object):
    help_queries=["billing","billing_prompt","customer_history","record_actions","autosuggest_mechanism","list_of_items"]
    def __init__(self,file_name="help_main.txt",subfolder_name="help_user_data"):
        self.file_name=file_name
        self.subfolder_name=subfolder_name
    def get_data(self):
        #This parent folder system is used so that the file is still accessible when we are running from terminal etc.
        #In a working directory approach, the working directory will change as the location of running will change...
        parent_dir=Path(__file__).resolve().parent
        file_path=parent_dir / self.subfolder_name / self.file_name
        with open(file_path,"r") as f:
            data=f.read()
        return data

class AutoSuggest(object):
    """
    Class used to handle the autosuggestion mechanism of the program...
    """
    def __init__(self,item,source):
        self.item=item
        self.source=source
    @classmethod
    def common(cls,a,b):
        """
        Checks how similar two strings are by using the Jaccard similarity method, and returns the similarity score to aid the autocorrect mechanism...
        :param a: first string
        :param b: second string
        :return: a similarity score to aid the autocorrect mechanism
        """
        count=len(set(a)&set(b))/len(set(a)|set(b))
        return count
    def autosuggest(self):
        """
        Checks the elements of the input source and determines the element closest to the input string...
        :return if the suggested item is close to the input element, closest: element closest to the input string,
            else if no item is close to the input element, None
        """
        closest=""
        count=0
        for i in self.source:
            b=AutoSuggest.common(self.item,i)
            if b>count:
                closest=i
                count=b
        if count>=0.5:
            return closest
        else:
            return None

#MISC FUNCTIONS
def process(x):
    a=str(x).split()
    if len(a)==0:
        return ""
    try:
        x = "".join(a)
        int(x)
        return x
    except ValueError:
        if len(a)==1:
            return a[0].lower()
        else:
            temp=a[0]
            for i in a[1::]:
                temp=temp+" "+i
            return temp.lower()

def process_name(name):
    name=str(name).lower().split()
    output=name[0].lower()
    if len(output)==1:
        return output[0].capitalize()
    for i in name[1::]:
        output=output+" "+i.capitalize()
    return output

def validate_number(x):
    try:
        assert int(x)>0
        if len(str(x))==10:
            return {"error":False}
        else:
            return {"error":True,"type":"invalid_format"}
    except (ValueError,AssertionError):
        return {"error":True,"type":"invalid_type"}

def mob_type_error_UI(mob,error):
    match error:
        case "invalid_type":
            print("Invalid number!")
            print("Please enter correct number: ",end=" ")
            a=input()
            return a
        case "invalid_format":
            print("Number is invalid!")
            try:
                assert len(str(mob))>=10
                a=str(mob)[0:10:]
                while True:
                    print(f"Did you mean {a}? (y/n)")
                    x=process(input())
                    if x=="y" or x=="yes" or x=="yeah":
                        return a
                    elif x=="n" or x=="no" or x=="nah":
                        print("Enter correct number: ",end="")
                        a=input()
                        return a
                    else:
                        print("Enter y or n...")
            except AssertionError:
                print("Enter correct number: ", end="")
                a = input()
                return a
        case _:
            return -1

def correct_mobile(incorrect_mob: str):
    corr_num = False
    while not corr_num:
        mob_status=validate_number(incorrect_mob)
        if mob_status["error"]:
            match mob_status["type"]:
                case "invalid_type":
                    incorrect_mob=process(mob_type_error_UI(incorrect_mob,"invalid_type"))
                case "invalid_format":
                    incorrect_mob=process(mob_type_error_UI(incorrect_mob,"invalid_format"))
        elif not mob_status["error"]:
           corr_num=incorrect_mob
    return corr_num

def auto_suggest_handler(source: list, item: str):
    autosugg_obj=AutoSuggest(item,source)
    sugg_item=autosugg_obj.autosuggest()
    return sugg_item

def auto_suggest_ui(sugg_item):
    if not sugg_item:
        return -2
    print(f"Did you mean {sugg_item}? (y/n)",end=" ")
    while True:
        ask=process(input())
        match ask.lower():
            case "y" | "ya" | "yeah" | "yes" | "yuh uh":
                return sugg_item
            case "n" | "nah" | "nuh uh" | "no" | "nope":
                return -1
            case _:
                print("Enter (y/n): ",end="")

#BILLING PART
def billing_UI_intro():
    """
    The function which handles the UI part of the billing process by taking user input regarding the billing details
    :return the user input...
    """
    print("Enter name of customer: ",end="")
    cust_name=input()
    print("Enter mobile number: ",end="")
    mobile=input()
    other_data = {"customer_name": cust_name, "customer_num": mobile}
    print("-"*64)
    return other_data

def billing_UI_prompt():
    print("PROMPT BELOW...")
    input_list=[]
    while True:
        x=input(">>> ")
        if x=="":
            break
        elif x.replace(" ","")=="":
            continue
        x=list(process(x).split(" "))
        input_list.append(x)
    return input_list

def bill_process(cashier,element):
    """
    Used to process the individual elements of the user input... It does the main parsing of the element, and accordingly it calls bill methods...
    :param cashier: a cashier object
    :param element: the input element to process
    :return: if an error has occurred, the context of the problem...
    """
    match element[0].lower():
        case "r" | "rem" | "remove" | "d" | "delete":
            try:
                a=cashier.rem_item(process(element[1]))
            except IndexError:
                return {
                    "error": True,
                    "type": "invalid_format",
                    "function": "removing item",
                    "quantity": None,
                }
            if a==-1:
                return {
                    "error":True,
                    "type":"item_not_billed",
                    "function":"removing item",
                    "quantity":None,
                    }
        case "e" | "edit" | "update":
            try:
                if element[2].replace(" ", "") == "":
                    quan = 1
                else:
                    quan = int(process(element[2]))
                assert quan > 0
            except IndexError:
                quan=1
            except (ValueError,AssertionError):
                return {
                    "error": True,
                    "type": "invalid_quantity",
                    "function": "editing quantity"
                }
            try:
                a=cashier.edit_quan(process(element[1]),quan)
            except IndexError:
                return {
                    "error": True,
                    "type": "invalid_format",
                    "function": "editing quantity",
                    "quantity": None,
                }
            if a==-1:
                return {
                    "error":True,
                    "type":"item_not_defined",
                    "function":"editing quantity",
                    "quantity":quan,
                    }
            
        case _:
            try:
                if element[1].replace(" ","") == "":
                    quan=1
                else:
                    quan=int(process(element[1]))
                assert quan>0
            except IndexError:
                quan=1
            except (ValueError,AssertionError):
                return {
                    "error": True,
                    "type": "invalid_quantity",
                    "function": "billing"
                }
            a=cashier.billing(process(element[0]),quan)
            if a==-1:
                return {
                    "error":True,
                    "type":"item_not_defined",
                    "function":"billing",
                    "quantity":quan,
                    }
    return {"error":False}

def bill_header():
    print("-"*64)
    print(f"{"ANANT'S CASHIER SOFTWARE":^64}")
    print("-"*64)

def display_bill(items: dict[str,list[int]], total: int =0, other_data :dict | None =None):
    """
    Used to display the billing details to the user in an organized manner
    :param items: the items which are to be displayed
    :param total: the total monetary amount
    :param other_data: other data regarding the transaction details -> cashier name, customer name, customer mob
    :return: None
    """
    print("-"*64)
    if other_data:
        print(f"{other_data["date_time_info"]}\nCashier: {process_name(other_data["cash_name"])}\nCustomer: {process_name(other_data["cust_name"])}\nMobile:{other_data["cust_mob"]}")
        print("-" * 64)
    if not items:
        print("No data available...")
        return
    print(f"{"ITEM NAME":22}{"RATE":6}{"QUANTITY":10}{"AMOUNT":5}")
    print("-"*64)
    for i,j in items.items():
        a=i
        b=j[0]
        c=j[1]
        print(f"{a:20}{c:5}{b:10}{b*c:5}")
    print("-"*64)
    print(f"TOTAL={total}")
    print(f"TOTAL ITEMS PURCHASED={len(items)}")
    print("-"*64)

def bill_confirmation()->bool:
    """
    This function allows the user to confirm the bill ie the bill will be saved or cancel the bill ie the bill will not be saved.
    """
    print("-"*64)
    while True:
        print("Confirm bill? (y/n) ", end="")
        conf=process(input(""))
        match conf:
            case "y"|"yes"|"ya"|"yeah"|"yuh uh":
                return True
            case "n"|"no"|"na"|"nuh uh":
                print("Cancelling...")
                return False
            case _:
                print("Please enter yes or no...")


def billing_error_messages(error, details=None):
    print("-" * 64)
    match error:
        case "item_not_defined":
            print(f"{details} not defined!")
        case "invalid_quantity":
            print("The quantity is not valid! The quantity must be an integer greater than 0.\nSee help page for more information...")
            print(f"Error has occurred during {details}!")
        case "invalid_format":
            print("The format is not valid!\nSee help page for information regarding the format of billing prompt requests...")
        case "no_data_entered":
            print("No data entered into billing prompt!\nSee help page for more information...")
        case "no_items_list":
            print("No items list was found! Try resetting the csv file in the manage loi section...\nSee help page for more information...")
        case "no_item_suggested":
            print("No item could be suggested for the given input...")
        case "sugg_item_rejected":
            print("The suggested item was rejected...")
        case "item_not_billed":
            print("The item did not exist in bill!\nNo item found to remove...")
        case _:
            print("An error occurred...")

def main_bill_controller(cash_name):
    """
    The main controller which handles the billing process by calling other billing methods...
    It is used to control the flow of the billing process
    :param cash_name: the name of the cashier
    :return: None
    """
    if not Cashier.LoI:
        billing_error_messages("no_items_list")
        return

    other_data = billing_UI_intro()
    input_number = other_data["customer_num"]

    corr_mob = correct_mobile(input_number)
    cash_data=list(map(process,[cash_name,other_data["customer_name"],corr_mob]))

    #Main Billing Handle
    input_list=billing_UI_prompt()
    if not input_list:
        billing_error_messages("no_data_entered")
        return
    cashier=Cashier(cash_data[0],cash_data[1],cash_data[2])
    wrong_input={}
    for i in input_list:
        status=bill_process(cashier,i)
        if status["error"] and status["type"] == "item_not_defined":
            wrong_name = cashier.item
            if wrong_name not in wrong_input.keys():
                billing_error_messages("item_not_defined", cashier.item)
                sugg_item = auto_suggest_ui(auto_suggest_handler(item=wrong_name, source=list(Cashier.LoI.keys())))
                if sugg_item == -2:
                    billing_error_messages("no_item_suggested")
                elif sugg_item == -1:
                    billing_error_messages("sugg_item_rejected")
                wrong_input.update({wrong_name: sugg_item})
            sugg_item = wrong_input[wrong_name]
            if sugg_item not in [-1, -2]:
                match status["function"]:
                    case "billing":
                        status=bill_process(cashier, [sugg_item, str(status["quantity"])])
                    case "removing item":
                        status=bill_process(cashier, ["r", sugg_item])
                    case "editing quantity":
                        status=bill_process(cashier, ["e", sugg_item, str(status["quantity"])])
            elif sugg_item in [-1,-2]:
                continue
        if status["error"]:
            billing_error_messages(status["type"],status["function"])
    if bill_confirmation():
        pass
    else:
        return
    bill_header()
    display_bill(cashier.items,cashier.total())
    if not cashier.items:
        return
    trans_data=cashier.get_transaction()
    record_handle=RecHandler(trans_data)
    record_handle.update_rec()
    return

#RECORD PART
def rec_UI():
    """
    Used to interact with the user and retrieve input regarding what action the user wants to perform regarding the record file...
    :return: the user input action
    """
    print("-" * 64)
    print("Enter 1 to retrieve specific customer transaction record\n2 to retrieve entire customer record\n3 to delete entire customer record\n4 to exit record management loop")
    try:
        choice=int(input())
    except ValueError:
        print("Integer value was expected!")
        return None
    match choice:
        case 1:
            cust = process(input("Enter name of customer: "))
            mobile = process(input("Enter mobile number: "))
            return {
                "action":"specific_cust_data",
                "cust_name":cust,
                "cust_mobile":mobile
            }
        case 2:
            return {
                "action":"all_cust_data"
            }
        case 3:
            return {
                "action":"del_cust_data"
            }
        case 4:
            return {
                "action":"exit_loop"
            }
        case _:
            return {
                "action":"action_not_recognised"
            }

def get_spec_rec(name,number):
    """
    to get the transaction details of a specific customer...
    :return: the transaction details of the customer
    """
    trans_data=RecHandler.retrieve_cust(name,number)
    return trans_data

def get_all_rec():
    """
    used to get the entire record of the transaction as available in the record file...
    :return: the transaction data
    """
    data=RecHandler.get_rec()
    return data

def conf_del_rec():
    """
    used to confirm whether the customer really wants to delete the data
    :return: the user choice
    """
    print("Are you sure you want to delete record? (y/n)")
    while True:
        user_input=process(input())
        match user_input.lower():
            case "y" | "yes" | "yeah" | "ya":
                return True
            case "n" | "no" | "nah":
                return False
            case _:
                print("Enter (y/n)... to do nothing, enter (n) [without the brackets]...")

def rec_user_output(action):
    print("-" * 64)
    match action:
        case "del_cust_data":
            print("Deleting customer record...")
        case "exit_loop":
            print("Exiting...")
        case "action_not_recognised":
            print("Action not recognised!\nRead the given instructions carefully...")
        case _:
            print("Action completed successfully!")
def rec_controller():
    """
    The main controller which handles the record handling process by calling other billing methods...
    It is used to control the flow of the record handling process and allows the user to modify the existing record...
    :return: None
    """
    while True:
        status=rec_UI()
        if status:
            match status["action"]:
                case "specific_cust_data":
                    mobile=correct_mobile(status["cust_mobile"])
                    trans_info=get_spec_rec(status["cust_name"],mobile)
                    if trans_info:
                        for i in trans_info:
                            display_bill(i["items"],i["total"],i)
                    else:
                        display_bill({})
                case "all_cust_data":
                    trans_info = get_all_rec()
                    if trans_info:
                        for i in trans_info:
                            display_bill(i["items"], i["total"], i)
                    else:
                        display_bill({})
                case "del_cust_data":
                    conf=conf_del_rec()
                    if conf:
                        RecHandler.del_rec()
                    rec_user_output("del_cust_data")
                case "exit_loop":
                    rec_user_output("exit_loop")
                    break
                case "action_not_recognised":
                    rec_user_output("action_not_recognised")
#HELP HANDLE
def help_input_UI():
    print(">>> ",end="")
    query=input()
    return query

def help_retrieve_data(filename):
    file=HelpHandler(filename)
    file_data=file.get_data()
    return file_data

def help_process_query(query)->dict[str, bool | str]:
    queries_list=HelpHandler.help_queries
    elements=query.lower().split(".")
    try:
        assert len(elements)==2 and elements[0] == "help"
        if elements[1]=="exit":
            return {"error":False,"exit":True}
        elif elements[1] in queries_list:
            return {"error":False,"exit":False,"file_name":"help_"+str(elements[1]+".txt")}
        else:
            return {"error":True,"error_msg":"invalid_query","string":elements[1]}
    except AssertionError:
        return {"error":True,"error_msg":"invalid_format","string":query}

def help_error_message(error_msg,query=None):
    match error_msg:
        case "invalid_query":
            print(f"Query '{query}' not recognised...")
        case "invalid_format":
            print("Invalid format! The recognised format is- 'help.<user_query>'. Please try again...")
        case "sugg_item_rejected":
            print("The suggested query was rejected...")
        case "no_item_suggested":
            print("No similar query could be found by autosuggest module...")
        case _:
            print("An unknown error has occurred! Please try again...")

def help_output(file):
    print("-" * 64)
    if file=="exit":
        print("Exiting help module...")
    else:
        print(file)
        print("-" * 64)

def help_controller():
    help_output(help_retrieve_data("help_main.txt"))
    while True:
        query=help_input_UI()
        processed=help_process_query(query)
        if processed["error"] and processed["error_msg"] == "invalid_query":
            help_error_message(processed["error_msg"],processed["string"])
            source_list = HelpHandler.help_queries
            source_list.append("exit")
            sugg_query = auto_suggest_ui(auto_suggest_handler(item=processed["string"], source=source_list))
            if sugg_query not in [-1, -2]:
                processed = help_process_query("help." + sugg_query)
            elif sugg_query == -1:
                help_error_message("sugg_item_rejected")
                continue
            elif sugg_query == -2:
                help_error_message("no_item_suggested")
                continue
        if processed["error"]:
            help_error_message(processed["error_msg"],processed["string"])
            continue
        try:
            if processed["exit"]:
                help_output("exit")
                break
        except KeyError:
            pass
        file_name=processed["file_name"]
        file_data=help_retrieve_data(file_name)
        help_output(file_data)

#LIST OF ITEMS MANAGEMENT PART
def manage_loi_input()->dict[str,str | int | bool]:
    """
    Takes user input regarding what action they want to perform,
    depending on the action, also takes input of necessary details needed for that action.
    :return: input details to the controller (can enter an error as 'choice' in case of invalid input)
    """
    print("-" * 64)
    choice=input("Enter 1 to display items list or retrieve price of specific item\n2 to add an item to the list\n3 to edit the price of an existing item\n4 to delete existing item or reset list\n5 to exit... \n-- ")
    try:
        choice=int(process(choice))
    except ValueError:
        choice=None
    match choice:
        case 1:
            print("Enter 1 to display items list, 2 to retrieve specific item price: ",end="")
            sub_choice=input()
            try:
                sub_choice=int(sub_choice)
            except ValueError:
                return {
                    "choice":"input_not_valid"
                }
            match sub_choice:
                case 1:
                    return {
                        "choice":"display_items"
                    }
                case 2:
                    name=process(input("Enter name of item: "))
                    return {
                        "choice":"specific_item",
                        "name":name
                    }
                case _:
                    return {
                        "choice":"input_not_valid"
                    }
        case 2:
            try:
                name, price= input("Enter name and price (separated by a comma) \nFormat: <item_name>, <price> where price is an integer...\n").split(",")
            except ValueError:
                return {
                    "choice":"input_not_valid"
                }
            return {
                "choice": "add_item",
                "item_name": process(name),
                "price": process(price)
            }
        case 3:
            try:
                name, price= input("Enter name and updated price (separated by a comma) \nFormat: <item_name>, <price> where price is an integer...\n").split(",")
            except ValueError:
                return {
                    "choice":"input_not_valid"
                }
            return {
                "choice": "edit_price",
                "item_name": process(name),
                "price": process(price)
            }
        case 4:
            print("Enter 1 to delete specific item, 2 to reset entire items list...")
            sub_choice=input()
            try:
                sub_choice = int(sub_choice)
            except ValueError:
                return {
                    "choice":"input_not_valid"
                }
            match sub_choice:
                case 1:
                    name = input("Enter name of item you want to delete: ")
                    return {
                        "choice": "delete_item",
                        "item_name": name
                    }
                case 2:
                    conf=input("Are you sure you want to reset list? \nAll changes made to the base list till date will be reset and inbuilt base list will remain. \nThis cannot be undone! \nDo you want to continue? (y/n): ")
                    match process(conf):
                        case "y" | "ya" | "yes" | "yeah":
                            return {
                                "choice":"reset_list",
                                "conf": True
                            }
                        case "n" | "na" | "no":
                            return {
                                "choice":"reset_list",
                                "conf": False
                            }
                        case _:
                            return {
                                "choice":"input_not_valid"
                            }
                case _:
                    return {
                        "choice":"input_not_valid"
                    }

        case 5:
            return {
                "choice": "exit_loop",
            }
        case _:
            return {"choice":"input_not_valid"}

def show_loi(menu: dict[str,int])->Exception | None:
    """
    Interacts with the class method to display the list of items to the user
    :param menu: The dictionary which contains the items and respective prices for displaying to the user
    :return: None if no error happened, or Exception if an error happened
    """
    print("-" * 64)
    print(f"{'Item':20} {'Rate':5}")
    try:
        for i,j in menu.items():
            print(f"{i:20} {j:5}")
        return None
    except Exception as e:
        return e

def loi_add_item(name: str,price: int)->dict[str,str|bool]:
    """
    Adds new item with price to the list of items by interacting with the class.
    :return: dictionary telling about error and type of error
    """
    check=ListOfItems.add_item(item=name,price=price)
    match check:
        case -1:
            return {
                "error": True,
                "type": "item_already_exists"
            }
        case 0:
            return {
                "error": False,
            }
        case _:
            return {
                "error": True,
                "type": "unknown"
            }

def loi_update_price(item: str,price: int)->dict:
    """
    Updates the price of an existing item in the csv file (list of items).
    :return: status about error, type of error and other important details
    """
    status=ListOfItems.edit_price(item,price)
    if status==-1:
        return {
            "error": True,
            "type": "item_not_found"
        }
    else:
        return {
            "error": False,
            "old_price": status
        }

def loi_delete_item(name:str | int)->dict[str,str|bool]:
    """
    Deletes an existing item in the csv file (list of items).
    If '-1' (integer) is passed as name, then it resets entire list
    :return: status about error and type of error
    """
    if name==-1:
        ListOfItems.reset_list()
        return {
            "error": False
        }

    status=ListOfItems.del_item(name)
    if status==-1:
        return {
            "error": True,
            "type": "item_not_found"
        }
    else:
        return {
            "error": False
        }

def loi_user_output(action: str, details: list | int= None):
    """Displays the final closing message for each action performed successfully..."""
    print("-" * 64)
    match action:
        case "add_item":
            print("Successfully added new item",end=" ")
            if details:
                print(f"'{details[0]}' with price {details[1]}!")
            else:
                print("!")
        case "edit_price":
            print("Successfully edited price",end=" ")
            if details:
                print(f"of '{details[0]}' from {details[1]} to {details[2]}!")
            else:
                print("!")
        case "delete_item":
            print("Successfully deleted item",end=" ")
            if details:
                print(f"'{details}'!")
            else:
                print("!")
        case "get_price":
            print(f"Price of '{details[0]}' is {details[1]}.")
        case "reset_list":
            if details:
                print(f"Successfully reset list...")
            else:
                print(f"Cancelling reset list...")
        case "exit_loop":
            print("Exiting...")

def retrieve_price(name: str)->dict[str,str | bool | int]:
    """
    Used to retrieve the price of a specific item from the items list
    :return: status about error and type of error or price of item in case of successful execution
    """
    status=ListOfItems.find_item(name)
    try:
        status=int(status)
    except ValueError:
        status=-2
    if status==-1:
        return {
            "error": True,
            "type": "item_not_found"
        }
    elif status==-2:
        return {
            "error": True,
            "type": "unknown"
        }
    else:
        return {
            "error": False,
            "price": status
        }

def loi_error_messages(error: str | bool | Exception =True):
    """
    Displays error messages regarding the items list (loi) management in the ui.
    """
    match error:
        case "invalid_price":
            print("Price is invalid!\nEnter an integer price...")
        case "item_already_exists":
            print("Item with that name already exists!")
        case "item_not_found":
            print("Item with that name not found!")
        case "input_not_valid":
            print("Input is not valid!\nCheck the given instructions carefully...")
        case "action_not_defined":
            print("Action not defined!\nEnter a valid action!")
        case "same_price":
            print("The saved price of item is same as entered price!\nThe price of the item is unchanged...")
        case "sugg_item_rejected":
            print("The suggested item was rejected!")
        case "no_item_suggested":
            print("No item could be suggested by autosuggest module!")
        case True:
            print("An error occurred!")
        case _:
            print(f"An error occurred: {error}")

def manage_loi_controller()->bool: #loi is List of Items
    changed=False
    while True:
        user_input=manage_loi_input()
        match user_input["choice"]:
            case "display_items":
                error=show_loi(ListOfItems.get_list())
                if error:
                        loi_error_messages(error)
            case "specific_item":
                name=user_input["name"]
                status=retrieve_price(name)
                if status["error"] and status["type"] == "item_not_found":
                    loi_error_messages(status["type"])
                    sugg_item = auto_suggest_ui(
                        auto_suggest_handler(item=user_input["name"], source=list(ListOfItems.get_list().keys())))
                    if sugg_item not in [-1, -2]:
                        name=sugg_item
                        status = retrieve_price(name)
                    elif sugg_item == -1:
                        loi_error_messages("sugg_item_rejected")
                        continue
                    elif sugg_item == -2:
                        loi_error_messages("no_item_suggested")
                        continue
                    else:
                        continue
                if status["error"]:
                    loi_error_messages(status["type"])
                    continue
                loi_user_output("get_price",[name,status["price"]])
            case "add_item":
                name,price =user_input["item_name"],user_input["price"]
                try:
                    price=int(price)
                    assert price>=0
                except (ValueError,AssertionError):
                    loi_error_messages("invalid_price")
                    continue
                status=loi_add_item(name,price)
                if status["error"]:
                    loi_error_messages(status["type"])
                else:
                    loi_user_output("add_item",[name,price])
                    changed=True
            case "edit_price":
                name, price= user_input["item_name"],user_input["price"]
                try:
                    price = int(price)
                    assert price > 0
                except (ValueError, AssertionError):
                    loi_error_messages("invalid_price")
                    continue
                status=loi_update_price(name,price)
                if status["error"] and status["type"] == "item_not_found":
                    loi_error_messages(status["type"])
                    sugg_item = auto_suggest_ui(auto_suggest_handler(item=name, source=list(ListOfItems.get_list().keys())))
                    if sugg_item not in [-1, -2]:
                        name=sugg_item
                        status = loi_update_price(name, price)
                    elif sugg_item == -1:
                        loi_error_messages("sugg_item_rejected")
                        continue
                    elif sugg_item == -2:
                        loi_error_messages("no_item_suggested")
                        continue
                    else:
                        continue
                if status["error"]:
                    loi_error_messages(status["type"])
                    continue
                if status["old_price"]==price:
                    loi_error_messages("same_price")
                else:
                    loi_user_output("edit_price",[name,status["old_price"],price])
                    changed=True
            case "delete_item":
                name=user_input["item_name"]
                status = loi_delete_item(name)
                if status["error"] and status["type"] == "item_not_found":
                    loi_error_messages(status["type"])
                    sugg_item = auto_suggest_ui(auto_suggest_handler(item=name, source=list(ListOfItems.get_list().keys())))
                    if sugg_item not in [-1, -2]:
                        name = sugg_item
                        status = loi_delete_item(name)
                    elif sugg_item == -1:
                        loi_error_messages("sugg_item_rejected")
                        continue
                    elif sugg_item == -2:
                        loi_error_messages("no_item_suggested")
                        continue
                    else:
                        continue
                if status["error"]:
                    loi_error_messages(status["type"])
                    continue
                loi_user_output("delete_item", name)
                changed=True
            case "reset_list":
                if user_input["conf"]:
                    ListOfItems.reset_list()
                    loi_user_output("reset_list",1)
                    changed=True
                else:
                    loi_user_output("reset_list",0)
            case "exit_loop":
                loi_user_output("exit_loop")
                break
            case "input_not_valid":
                loi_error_messages("input_not_valid")
            case _:
                loi_error_messages("action_not_defined")
    return changed

#MAIN PART
def main_UI_welcome():
    """
    The welcome screen which allows the user to enter cashier name
    :return name: name of the cashier
    """
    print("-"*64)
    print("Welcome to Cashier software!!")
    print("-"*64)
    name=input("Enter name of cashier: ")
    print("Processing...")
    return name

def main_UI_loop():
    """
    Allows the user to interact with the program in a looping structure and use the features the program has to offer...
    :return: whether an error has occurred or not, and the user input...
    """
    print("-" * 64)
    print("Enter 1 to create bill\n2 for customer record actions\n3 to learn more about the program\n4 to enter items management menu\n5 to exit cashier program")
    try:
        choice=int(input())
    except ValueError:
        return {"error":"input_not_valid"}
    action_list={1:"create_bill",2:"record_actions",3:"help_window",4:"items_list",5:"exit_loop"}
    try:
        return {"error":None,"action":action_list[choice]}
    except (IndexError,KeyError):
        return {"error":"input_not_valid"}

def main_error_handle(error):
    """
    Used to handle the errors which can occur while interacting with the user...
    """
    match error:
        case "input_not_valid":
            print("Enter valid input...")
        case "unknown_error":
            print("An unknown error has occurred...")
        case _:
            print("An unknown error has occurred...")

def exit_handle():
    """
    Used to display exit message when the program is ending...
    :return: None
    """
    print("-" * 64)
    print("Exiting...")
    print("Thank you for using cashier software!")
    print("-" * 64)
def main_controller():
    """
    The main controller which handles the main program and calls various methods based on user input...
    :return: None
    """
    cash_name=main_UI_welcome()
    while True:
        user_choice=main_UI_loop()
        if user_choice["error"]:
            main_error_handle(user_choice["error"])
            continue
        match user_choice["action"]:
            case "create_bill":
                main_bill_controller(cash_name)
            case "record_actions":
                rec_controller()
            case "help_window":
                help_controller()
            case "items_list":
                loi_changed=manage_loi_controller()
                if loi_changed:
                    Cashier.refresh_LoI()
            case "exit_loop":
                exit_handle()
                break
            case _:
                main_error_handle("unknown_error")

if __name__ == '__main__':
    try:
        main_controller()
    except KeyboardInterrupt:
        exit_handle()
