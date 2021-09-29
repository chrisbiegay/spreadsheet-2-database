# Overview
Utility for dumping a CSV or Excel file into a SQLite database.


# Prerequisites
* Python 3.x is installed and on the execution path.


# Environment Setup
    python3 -m venv .venv               # Run if the .venv directory does not already exist
    source .venv/bin/activate           # Activate the Python virtual environment in the current shell
    pip install -r requirements.txt     # Run once after creating the .venv directory in step 1


# Running the App
Make sure the python environment is set up first.

Run this example command from within the `spreadsheet-2-database` directory:

    ./spreadsheet2db.sh example/example1.csv

To see the program usage:

    ./spreadsheet2db.sh -h


# IntelliJ Setup
1. Make sure the `.venv` directory has been created already.
2. Open the project directory with `File -> Open...`.
3. Follow the prompts to set up the Python SDK for the project, and specify the python
   executable under `.venv/bin`.
