# Part B – Implementation & Task Distribution

**Global Deadline:** Wednesday, May 7, 2025

## Tools & Knowledge Needed
- MySQL server installed and running
- Python 3.x installed
- Python package: mysql-connector-python (or equivalent DB driver)
- IDE or code editor (VS Code, PyCharm, etc.)
- Basic understanding of SQL and Python database connectivity

## First Steps
- Initialize a Git repository and push to GitHub with a simple naming scheme.
- Create README.md with a one-paragraph overview.
- Define naming conventions: snake_case for SQL tables/columns and Python modules/functions.

- Create a `smoke_test.py` that connects to `library_db`, runs `SELECT COUNT(*) FROM books;`, and prints "OK" or the error.
- Plan a 15-minute team review after CRUD is implemented to demo functions and align on next steps.

## Part B Task List

1. Prepare SQL Schema (DDL) – 3 hours
   - Write `CREATE TABLE` scripts for all tables
   - Define PKs, FKs, data types, constraints
   - Install MySQL server
   - Create `library_db` database in MySQL
   - Save your `CREATE TABLE` scripts to a file named `schema.sql`

2. Seed with Dummy Data (DML) – 2 hours
   - Craft `INSERT INTO` scripts for typical and edge-case records
   - Write `INSERT INTO` statements in `data.sql`
   - Load data via the MySQL client using `source data.sql`
   - Verify inserted records using `SELECT *`

3. Initialize DB Programmatically – 2 hours
   - Write setup module to run DDL & DML in code
   - Check Python installation with `python --version`
   - Install the DB driver: `pip install mysql-connector-python`
   - Write a script `init_db.py` to execute `schema.sql` and `data.sql`
   - Run `python init_db.py` to initialize the database

4. Implement CRUD Operations – 5 hours
   - Create, Read, Update, Delete functions for each entity
   - Create a module `crud.py` with functions: `add_book()`, `get_book()`, `update_member()`, `delete_loan()`, etc.
   - Write simple test calls at the bottom of `crud.py` to verify each function
   - Log success or errors to the console

5. Draft Part B Report – 6 hours
   - Include schema and data excerpts from schema.sql and data.sql
   - Document 3–5 key SQL queries (SELECT, UPDATE, DELETE) with purpose, descriptions, and query outputs
   - Present code snippets from init_db.py and crud.py highlighting setup and CRUD logic
   - Embed screenshots of menu-driven CRUD operations and sample terminal outputs
   - Detail team contributions for each report section



## Optional Tasks
- **Advanced Query Features**  
  - Parameterized filtering, sorting, and complex joins  
  - ⏱️ Estimated: 2 hours
- **User Authentication**  
  - Design `Users` table and implement login/logout flow  
  - ⏱️ Estimated: 2 hours
- **GUI Interface**  
  - Sketch and implement screens for login, CRUD operations, and reports  
  - ⏱️ Estimated: 4 hours
