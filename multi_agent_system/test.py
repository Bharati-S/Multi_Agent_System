
import sqlite3

def show_tables_and_data(db_path):
    # Connect to your SQLite database file
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in database:")
    for table_name in tables:
        print(f"- {table_name[0]}")

    # For each table, fetch and print first 5 rows
    for table_name in tables:
        print(f"\nData from table '{table_name[0]}':")
        cursor.execute(f"SELECT * FROM {table_name[0]} LIMIT 5;")
        rows = cursor.fetchall()

        # Get column names
        col_names = [description[0] for description in cursor.description]

        # Determine max width per column (based on header or max data length in the sample rows)
        col_widths = []
        for i, col in enumerate(col_names):
            max_len = len(col)
            for row in rows:
                cell_len = len(str(row[i]))
                if cell_len > max_len:
                    max_len = cell_len
            col_widths.append(max_len + 2)  # add padding

        # Print header row with padding
        header_row = ""
        for i, col in enumerate(col_names):
            header_row += f"{col:<{col_widths[i]}}"
        print(header_row)
        print("-" * sum(col_widths))

        # Print rows with padding
        for row in rows:
            row_str = ""
            for i, cell in enumerate(row):
                row_str += f"{str(cell):<{col_widths[i]}}"
            print(row_str)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    db_path = r"C:/multi_agent_system/shared_memory.db"  
    show_tables_and_data(db_path)
