# Currency Handler (Python Lab)

Small Python project from my _Python Programming for MLOps_ course.  
The goal of the lab was to practice building a simple, maintainable Python program with clear separation of concerns (entrypoint vs. business logic) and basic persistence/logging.

## What it does

- Runs a currency-handling workflow via a CLI/terminal entrypoint (`main.py`)
- Contains the core logic in a separate module (`currencyhandler.py`)
- Stores runtime output / logs in a JSON file (`currency_log.json`)

> Note: This is a course lab project. The focus is on code structure, readability, and correctness.

## Tech

- Python 3.x
- JSON for simple storage/logging

## Project structure

````text
lab2-BigLurch/
    main.py                 # Program entrypoint
    currencyhandler.py      # Core currency logic
    currency_log.json       # Log/output persisted as JSON
    readme.md               # This file
````

### How to run
1) Create and activate a virtual environment

macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
````

Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install requirements.txt

```bash
pip install -r requirements.txt
```

3. Run the program

```bash
python main.py
```
