LibraryMS

A CSCI 331 group project: a simple library-management database system built with MySQL and Python.

Prerequisites
	•	MySQL server installed and running
	•	Python 3.x installed
	•	mysql-connector-python (or equivalent) installed via pip
	•	Git for version control

First Steps
	1.	Clone the repo and create your branch:
git clone https://github.com/cmbarrosb/LibraryMS.git
cd LibraryMS/PartB
git checkout -b feature/your-task
	2.	Scaffold directories:
/sql        ← schema.sql, data.sql
/src        ← init_db.py, crud.py
PartB_Task_Distribution.md
README.md
	3.	Commit and push your branch:
git add .
git commit -m “scaffold project structure”
git push -u origin feature/your-task

Setup
	1.	Create the database and tables:
mysql -u  -p < sql/schema.sql
	2.	Load dummy data:
mysql -u  -p < sql/data.sql
	3.	(Optional) Programmatic setup:
pip install mysql-connector-python
python src/init_db.py

Usage
	•	Smoke test:
python src/smoke_test.py
	•	CRUD demo:
python src/crud.py
	•	Full plan: see PartB_Task_Distribution.md

Project Structure

LibraryMS/
├─ PartB/
│  ├─ sql/
│  │  ├─ schema.sql
│  │  └─ data.sql
│  ├─ src/
│  │  ├─ init_db.py
│  │  └─ crud.py
│  ├─ PartB_Task_Distribution.md
│  └─ README.md
└─ (other files…)

Contributing
	1.	Create a feature branch (feature/xyz)
	2.	Implement changes & commit often
	3.	Push and open a PR against main
	4.	Peer-review & merge
