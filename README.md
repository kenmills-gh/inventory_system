# inventory_system# Inventory Management System

A full-stack Python application featuring a **Flask REST API backend**, live external **OpenFoodFacts API integration**, an interactive **Command-Line Interface (CLI) frontend**, and a comprehensive **Pytest testing suite**.

## 🛠️ Installation & Setup

### Prerequisites
    * Python 3.10+
    * Pipenv

---

### Getting Started
Clone the repository:
```bash
    git clone [https://github.com/your-username/inventory-management-system.git](https://github.com/your-username/inventory-management-system.git)
    cd inventory-management-system
```

---

## Install Dependencies

``` bash
pipenv install
pipenv shell
```
---

## 🏃‍♂️ Running the Application

### This project runs a client-server architecture. You will need two terminal windows.

* Terminal 1: Start the Flask Backend Server (The server will start listening on http://127.0.0.1:5000)
``` bash
python app.py 
```

* Terminal 2: Run the Interactive CLI Frontend
Make sure your pipenv shell is active, then launch the CLI:
``` bash
python cli.py
```

--- 

## 🧪 Running Tests

* To run the complete automated test suite using pytest:
```bash
pytest
```
---

## 🚀 Features

* **Flask REST API Backend (`app.py`)**:
  * Implements full CRUD functionality (`GET`, `POST`, `PATCH`, `DELETE`) for managing inventory stock and pricing.
  * Dynamically fetches product metadata (product name, brands, ingredients) from the live OpenFoodFacts API upon creation.
  * Robust error handling with appropriate HTTP status codes (`200`, `201`, `404`).
* **Interactive CLI Frontend (`cli.py`)**:
  * Provides a user-friendly menu loop with 7 distinct options.
  * Features custom **card-style formatting** complete with emojis, structured labels, and formatted currency for optimal user experience.
  * Validates numeric input types (stock integers and floats for pricing).
* **Automated Test Suite (`tests/test_app.py`)**:
  * Built using `pytest` and Flask's test client.
  * 100% test coverage validating all CRUD routes, external API endpoints, and `404` error states.

---

## 📁 Project Structure

```text
inventory-management-system/
│
├── app.py              # Flask REST API server and mock database
├── cli.py              # Interactive Command-Line Interface frontend
├── Pipfile             # Pipenv dependency configuration
├── Pipfile.lock        # Pipenv lock file
├── README.md           # Project documentation
├── .gitignore          # Git exclusion rules
└── tests/              
    └── test_app.py     # Pytest unit and integration test suite