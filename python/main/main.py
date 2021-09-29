import argparse
import os
import os.path
import re
import pandas as pd
import sqlite3


DEFAULT_TABLE_NAME_FOR_CSV = "csv_data"
OUTPUT_FILE_PATH = "out/output-sqlite.db"
PROGRAM_NAME = "spreadsheet2db.sh"


def main():
    program_args = parse_program_args()

    # load a dictionary of spreadsheet names mapped to their corresponding pandas dataframes
    sheets_to_dfs = load_spreadsheet_file_into_dataframes(program_args.input_file_path, program_args.delim)

    if os.path.isfile(OUTPUT_FILE_PATH):
        os.remove(OUTPUT_FILE_PATH)

    db_conn = None
    print(f'Writing SQLite database to "{OUTPUT_FILE_PATH}"...')

    try:
        db_conn = sqlite3.connect(OUTPUT_FILE_PATH)
        cur = db_conn.cursor()

        for sheet_name, sheet_df in sheets_to_dfs.items():
            table_name = sanitize_name_for_sql(sheet_name)
            sanitize_column_names_for_sql(sheet_df)
            column_names = sheet_df.columns.to_list()
            cur.execute(f"CREATE TABLE {table_name} ({' text, '.join(column_names)} text)")
            sheet_df.to_sql(table_name, db_conn, if_exists="append", index=False)

        db_conn.commit()
    finally:
        if db_conn:
            db_conn.close()

    print("Done")


def parse_program_args():
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME,
                                     description="Load a CSV or Excel file into a SQLite database file.")
    parser.add_argument("input_file_path", metavar="INPUT_FILE_PATH", help="Path to the CSV or Excel file.")
    parser.add_argument("--delim", default=",",
                        help="Specifies the CSV delimiter. The default is comma (,). "
                             + "Examples: \"--delim ';'\" OR \"--delim tab\". "
                             + 'Note that the word "tab" can be used for tab-delimited files.')
    args = parser.parse_args()

    if args.delim == "tab":
        args.delim = "\t"

    return args


def load_spreadsheet_file_into_dataframes(input_file_path, csv_delimiter):
    """
    Loads the specified CSV or Excel file into a map of sheet names to their corresponding dataframes.
    In the case of CSVs a default sheet name is used.

    :param input_file_path: the path to the input file.
    :param csv_delimiter: the delimiter to be used if the file is a CSV.
    :return dict: a dictionary of sheet names to their corresponding dataframes.
    """

    if input_file_path.lower().endswith("csv"):
        print("Reading input file as CSV...")
        df = pd.read_csv(input_file_path, delimiter=csv_delimiter)
        sheet_to_df_map = {DEFAULT_TABLE_NAME_FOR_CSV: df}
    else:
        print("Reading input file as Excel...")
        excel_file = pd.ExcelFile(input_file_path)
        sheet_to_df_map = {}
        for sheet_name in excel_file.sheet_names:
            print(f"  Reading sheet '{sheet_name}'...")
            sheet_to_df_map[sheet_name] = pd.read_excel(excel_file, sheet_name)

    return sheet_to_df_map


def sanitize_name_for_sql(sheet_name):
    if sheet_name[0].isdigit():
        sheet_name = "_" + sheet_name

    return re.sub(r"\W", "_", sheet_name)


def sanitize_column_names_for_sql(sheet_df):
    for col_name in sheet_df.columns.to_list():
        sheet_df.rename({col_name: sanitize_name_for_sql(col_name)}, axis="columns", inplace=True)


if __name__ == "__main__":
    main()
