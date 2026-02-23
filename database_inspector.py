import sqlite3

def print_table_data(table_name):
    con = sqlite3.connect('geogambler.db')
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    con.close()

con = sqlite3.connect('geogambler.db')
cursor = con.cursor()
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
for table in tables:
    print(f"Data from table: {table[0]}")
    print_table_data(table[0])
    print("\n")
