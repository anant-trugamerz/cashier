# Cashier

**A Python-based cashier and transaction management system.**

Cashier is a personal software project built to explore practical application development, clean architecture, transaction handling, and persistent data storage in Python.

Rather than being just a collection of functions, the project is designed around clearly separated responsibilities, making the application easier to maintain, extend, and eventually integrate with a graphical user interface.

## Features

- 🛒 **Menu Management** — Maintain an updatable product menu stored in CSV format, including item names and prices.
- 💰 **Transaction Processing** — Process purchases and calculate transaction totals.
- 📜 **Transaction History** — Persist transaction records using JSON.
- 🔎 **Smart Suggestions** — Suggest matching items using Jaccard similarity.
- 🧩 **Modular Architecture** — Separate cashier operations, transaction handling, record management, and item suggestions.
- 🖥️ **Terminal Interface** — Interact with the application through the command line.

> Features are being developed incrementally. The exact functionality depends on the current version.

## Architecture

Cashier is organized around separation of concerns, so individual components can be developed and maintained without turning the entire application into one giant function.

| Component     | Responsibility                                      |
| ------------- | --------------------------------------------------- |
| `Cashier`     | Coordinates the main cashier operations             |
| `Transaction` | Represents and handles transaction-related data     |
| `RecHandler`  | Manages transaction records and persistence         |
| `AutoSuggest` | Provides item suggestions using similarity matching |

The goal is to keep the user interface, business logic, and data storage as independent as practical.

## Tech Stack

- **Language:** Python
- **Menu Storage:** CSV for an editable, persistent product catalogue
- **Transaction Storage:** JSON for transaction records
- **Interface:** Command-line interface
- **Version Control:** Git and GitHub

## Getting Started

### Prerequisites

- Python 3.12 or a compatible Python version
- Git (optional, for cloning the repository)

### Installation

Clone the repository:

```bash
git clone https://github.com/anant-trugamerz/cashier
cd cashier
```

Run the application using the appropriate entry-point file:

```bash
python main.py
```

## Project Structure

The project is organized into separate components for transaction processing, record management, and item suggestions.

The exact file structure may evolve as the project develops.

## Development Roadmap

- [x] Build the core cashier and transaction management system
- [x] Implement persistent transaction history using JSON
- [x] Add an editable CSV-based product menu and item suggestions
- [ ] Expand billing functionality with taxes, discounts, and multiple payment methods
- [ ] Introduce invoice numbering and automatic stock management
- [ ] Improve terminal UI, menu navigation, and error handling
- [ ] Add menu and customer detail editing directly through the interface
- [ ] Build a graphical user interface using CustomTkinter

## Project Goals

Cashier is also a learning project focused on:

- Writing maintainable, modular Python code
- Understanding software architecture and separation of concerns
- Managing persistent application data
- Implementing practical algorithms
- Using Git and GitHub to track development

## Current Status

**In active development.**

The immediate focus is on improving the core functionality and refining the existing architecture before introducing a richer terminal interface.

## Author

**Anant** · [GitHub](https://github.com/anant-trugamerz)

Built as a personal project to learn software engineering through practical implementation.
