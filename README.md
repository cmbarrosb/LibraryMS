# LibraryMS

A CSCI 331 group project: a simple Library Management System built with MySQL and Python.

## Overview

This program initializes and manages a library database for Books, Copies, Members, Loans, and Staff. It includes scripts to set up the database schema, load sample data, and interact with the database via a text‑based menu for full CRUD (Create, Read, Update, Delete) operations.

## File Descriptions

- **sql/schema.sql**  
  Defines the database schema: tables, primary keys, and foreign-key constraints.

- **sql/data.sql**  
  Inserts dummy data into each table to facilitate testing and development.

- **src/init_db.py**  
  Prompts for your MySQL password, then creates or uses the `library_db` database and executes `schema.sql` and `data.sql` to initialize the database.

- **src/crud.py**  
  Contains modular CRUD functions for each entity (Book, Copy, Member, Loan, Staff). Launches an interactive submenu-driven interface to perform operations without writing SQL directly.

- **PartB_Task_Distribution.md**  
  Internal guide outlining Part B tasks, subtasks, and estimated time allocations.

- **README.md**  
  This file: provides an overview, setup instructions, and usage guide.

## Prerequisites

- MySQL server installed and running (e.g., via Homebrew on macOS).
- Python 3.13 installed.
- `mysql-connector-python` package installed:
  ```bash
  pip install mysql-connector-python
  ```
- Git for version control.

## Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/cmbarrosb/LibraryMS.git
   cd LibraryMS/PartB
   ```

2. **Install Python dependencies**  
   ```bash
   pip install mysql-connector-python
   ```

3. **Initialize the database**  
   ```bash
   python3.13 src/init_db.py
   ```
   **If you have multiple python installed in your system you might want to specify what version you want to run the python file Ex:**
   ```bash
   C:\users\UserName\appdata\local\programs\python\python311\python.exe src/init_db.py
   ```
   **Prompted to enter Password**
   - Enter your MySQL password when prompted.

## Configuration

By default, `src/init_db.py` uses a `USE_DEFAULT` flag set to `True`, which means it connects to:
- Host: localhost  
- User: root  
- Database: library_db  

and only prompts you for the MySQL password. If you need to customize the host, user, or database interactively, open `src/init_db.py` and set:
```python
USE_DEFAULT = False
```
at the top of the file.

## Data Loading Behavior

In `sql/data.sql`, all `INSERT INTO` statements have been changed to `INSERT IGNORE INTO`. This means:

- Duplicate‐key errors (e.g., inserting a row with an existing primary key) are converted into warnings, so the script continues without aborting.
- The seed script becomes idempotent: you can run it multiple times and only new, non-conflicting rows will be added.
- Any manual edits or existing data remain unchanged when re-running the data load.

## Usage

Launch the CRUD menu interface:

```bash
python3.13 src/crud.py
```

Follow on-screen prompts to manage:
- Books: add, view, list, update, delete  
- Copies: add, view, list, update, delete  
- Members: add, view, list, update, delete  
- Staff: add, view, list, update, delete  

## Project Structure

```
PartB/
├─ sql/
│  ├─ schema.sql
│  └─ data.sql
├─ src/
│  ├─ init_db.py
│  └─ crud.py
├─ PartB_Task_Distribution.md
└─ README.md
```

## Contributing

1. Create a feature branch:  
   ```bash
   git checkout -b feature/your-task
   ```
2. Commit your changes with descriptive messages.  
3. Push to GitHub and open a Pull Request against `main`.  
4. Peer review and merge.

*Good enough: get it working, then refine!*
