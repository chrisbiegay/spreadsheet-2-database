# Prerequisites
* Python 3.x and Pip are installed and in the execution path.


# Project creation steps
    mkdir spreadsheet-2-database
    cd spreadsheet-2-database
    python3 -m venv .venv               # create virtual Python environment
    source .venv/bin/activate           # activate the virtual Python environment in the current shell
    pip install pandas                  # install 3rd-party 'requests' module
    pip freeze > requirements.txt       # save module dependencies


# Working with the project
From within the spreadsheet-2-database directory:

    source .venv/bin/activate         # activate the virtual Python environment in the current shell
    pip install -r requirements.txt   # run this IF cloning this project for the first time
    make run                          # run the sample driver for the chris.netutils module
    make test                         # run the tests
    deactivate                        # deactivate the virtual Python environment when finished


# IntelliJ Setup
1. Open the project directory with `File -> Open...`.
2. Right-click the `python/main` directory and mark it as a Sources Root.
3. Right-click the `python/test` directory and mark it as a Test Sources Root.