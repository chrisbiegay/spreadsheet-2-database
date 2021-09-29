import os
import os.path
import re
import sys
import pandas as pd
import sqlite3

''' TODO
Refactor
keep old outputs and generate unique filename for new outputs
'''


ARG_INPUT_FILE_PATH = 'INPUT_FILE_PATH'
DEFAULT_TABLE_NAME_FOR_CSV = 'csv_data'
OUTPUT_FILE_PATH = 'out/output-sqlite.db'


def main():
    program_args = parse_program_args()
    input_filename = program_args[ARG_INPUT_FILE_PATH]

    if input_filename.lower().endswith('csv'):
        print('Reading CSV input file')
        df = pd.read_csv(input_filename)
        # dictionary of spreadsheet names to their corresponding dataframes
        sheet_to_df_map = {DEFAULT_TABLE_NAME_FOR_CSV: df}
    else:
        print('Reading Excel input file')
        excel_file = pd.ExcelFile(input_filename)
        # dictionary of spreadsheet names to their corresponding dataframes
        sheet_to_df_map = {}
        for sheet_name in excel_file.sheet_names:
            print(f'Reading sheet "{sheet_name}"')
            sheet_to_df_map[sheet_name] = pd.read_excel(excel_file, sheet_name)

    conn = None

    try:
        if os.path.isfile(OUTPUT_FILE_PATH):
            os.remove(OUTPUT_FILE_PATH)

        conn = sqlite3.connect(OUTPUT_FILE_PATH)
        cur = conn.cursor()

        print(f'Writing to: {OUTPUT_FILE_PATH}')

        for sheet_name in sheet_to_df_map:
            sheet_df = sheet_to_df_map[sheet_name]

            for col_name in sheet_df.columns.to_list():
                sheet_df.rename({col_name: sanitize_name_for_sql(col_name)}, axis='columns', inplace=True)

            table_name = sanitize_name_for_sql(sheet_name)
            column_names = sheet_df.columns.to_list()
            table_sql = f'CREATE TABLE {table_name} ({" text, ".join(column_names)} text)'

            cur.execute(table_sql)
            sheet_df.to_sql(table_name, conn, if_exists='append', index=False)
    finally:
        if conn:
            conn.close()

    print('Done')


def parse_program_args():
    if len(sys.argv) < 2:
        print_usage_and_exit()

    return {ARG_INPUT_FILE_PATH: sys.argv[1]}


def print_usage_and_exit():
    print('Usage: python main.py <input_file_path>')
    sys.exit(1)


def sanitize_name_for_sql(sheet_name):
    return re.sub(r'\s', '_', sheet_name)


if __name__ == '__main__':
    main()
