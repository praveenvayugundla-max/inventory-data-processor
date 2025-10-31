# 🧾 Inventory Data Processor & Management System

This repository contains two stages of development for an inventory management tool created during Week 1 and Week 2 training.

---

## 🗓️ Week 1 — Inventory Data Processor (Procedural)

### 🎯 Objective
Create a command-line utility that:
- Reads inventory data from `inventory.csv`
- Validates rows using **Pydantic**
- Logs invalid data to `errors.log`
- Generates a `low_stock_report.txt` for items with low quantity

### ⚙️ Features
- ✅ CSV file handling with the `csv` module  
- ✅ Validation (`quantity ≥ 0`, `price > 0`) using Pydantic  
- ✅ Error logging with timestamps  
- ✅ Type hints and docstrings for clarity  
- ✅ Follows **Single Responsibility Principle (SRP)**  

### 📂 Example Project Structure
```
inventory-data-processor/
├── inventory.csv
├── main.py
├── errors.log
├── low_stock_report.txt
├── requirements.txt
└── README.md
```

### 🧠 Key Concepts
CSV handling · Pydantic validation · Exception handling · Logging · SRP · Type hinting · Docstrings  

---

## 🧱 Week 2 — Object-Oriented Inventory Management Package

### 🎯 Objective
Refactor the Week 1 script into a **modular OOP-based package** applying:
- Encapsulation, Inheritance, and Polymorphism  
- Open/Closed Principle (OCP)  
- Factory and Singleton Design Patterns  
- Generators for memory-efficient data loading  

### 📁 Project Structure
```
inventory-data-processor/
├── inventory_manager/
│   ├── __init__.py
│   ├── config.py
│   ├── product.py
│   ├── factory.py
│   ├── inventory.py
│   └── report.py
├── outputs/
│   ├── low_stock_report.txt
│   └── errors.log
├── inventory.csv
├── .env
├── main.py
├── requirements.txt
└── README.md
```

## Week 3 — Automated Testing & Code Coverage
Objective

Add a comprehensive automated test suite for the entire package using Pytest and Test-Driven Development (TDD).

 ## Product Tests — Validations, setters, and computed values

 ## Inventory Tests — CSV loading, updates, low-stock logic

 ## Factory Tests — Correct subclass creation for product types

 ## Report Tests — Mocked file writes for safe testing

 ## Coverage Report — Achieved >93% coverage




 ## Test Structure

 tests/
├── conftest.py
├── test_product.py
├── test_inventory_io.py
├── test_inventory_update.py
├── test_inventory_value.py
└── test_factory.py
## Coverage Command
pytest --cov=inventory_manager --cov-report=term-missing -v

Example Output:
15 passed, 0 failed, 2 warnings
TOTAL COVERAGE: 93%


## Requirements

Python 3.10+

pydantic

python-dotenv

pytest, pytest-cov, pytest-mock









### ⚙️ Setup Instructions

#### 1️⃣ Create & Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

#### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
If you don’t have one:
```bash
pip install pydantic python-dotenv
```

#### 3️⃣ Create a `.env` File
```
INVENTORY_FILE=inventory.csv
REPORT_FILE=outputs/low_stock_report.txt
ERROR_LOG=outputs/errors.log
LOW_STOCK_THRESHOLD=10
```

#### 4️⃣ Run the Project
```bash
python -u main.py
```

Expected output:
```
📦 Inventory Management System (Week 2) Started...
✅ Loaded 4 products from inventory.csv
📄 Low-stock report generated at: outputs/low_stock_report.txt
🎯 Process complete!
```

---

## 🧩 Key Features
- Validation with **Pydantic v2**  
- **Encapsulation / Inheritance / Polymorphism**  
- **Factory Pattern** → Dynamic product creation  
- **Singleton Pattern** → ConfigLoader using `.env`  
- **Generator-based CSV loading** for performance  
- **Structured logging & report generation**  

---

## 🧠 Concepts Demonstrated

| Week | Focus | Core Topics |
|------|--------|-------------|
| **1** | Python Fundamentals | CSV processing, Pydantic, SRP |
| **2** | Object-Oriented Design | Classes, OCP, Factory, Singleton, Modules |

---

## 🧰 Requirements
- Python 3.10 or higher  
- `pydantic` v2+  
- `python-dotenv`

---

## 📄 License
Educational and training use only – Bitcot Labs Learning Program  

---

✨ **Author:** Praveen Vayugundla  
🚀 **Version:** Week 1 + Week 2 Completed
