# Overview
Utility for dumping a CSV or Excel file into a SQLite database.


# Prerequisites
* Python 3.x is installed and on the execution path.


# Working with the project
From within the spreadsheet-2-database directory:

    python3 -m venv .venv                       # Run if the .venv directory does not already exist
    source .venv/bin/activate                   # Activate the Python virtual environment in the current shell
    pip install -r requirements.txt             # Run once after creating the .venv directory in step 1
    make run input_file=example/example1.csv    # Run the program against example1.csv
    deactivate                                  # Deactivate the Python virtual environment when finished


# IntelliJ Setup
1. Make sure the `.venv` directory has been created already.
2. Open the project directory with `File -> Open...`.
3. Follow the prompts to set up the Python SDK for the project, and specify the python
   executable under `.venv/bin`.