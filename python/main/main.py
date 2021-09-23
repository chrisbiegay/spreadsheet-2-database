# import sys
# import chris.netutils
# Or: import chris.netutils as net
# Or: from chris.netutils import *

import os
import os.path
import sys
import pandas as pd
import sqlite3


DEFAULT_TABLE_NAME = 'data'
OUTPUT_FILE_PATH = 'out/output-sqlite.db'


class ProgramArgs:
    def set_input_file_path(self, path):
        self.input_file_path = path

    def get_input_file_path(self):
        return self.input_file_path

def main():
    program_args = parse_program_args()
    print('Reading input file')
    input_df = pd.read_csv(program_args.get_input_file_path())

    column_names = input_df.columns.to_list()
    print(f'Column Names: {column_names}')

    if os.path.isfile(OUTPUT_FILE_PATH):
        os.remove(OUTPUT_FILE_PATH)

    table_sql = f'CREATE TABLE {DEFAULT_TABLE_NAME} ({" text, ".join(column_names)} text)'
    print(f'CREATE TABLE SQL:\n  {table_sql}')
    
    try:
        conn = sqlite3.connect(OUTPUT_FILE_PATH)
        c = conn.cursor()
        print(f'Writing to: {OUTPUT_FILE_PATH}')
        c.execute(table_sql)
        input_df.to_sql(DEFAULT_TABLE_NAME, conn, if_exists='append', index=False)
    finally:
        if conn:
            conn.close()

    print('Done')


def parse_program_args():
    args = ProgramArgs()

    if len(sys.argv) < 2:
        print_usage_and_exit()

    args.set_input_file_path(sys.argv[1])
    return args


def print_usage_and_exit():
    print('Usage: python main.py <input_file_path>')
    sys.exit(1)


if __name__ == '__main__':
    main()
