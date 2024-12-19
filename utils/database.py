# database_utils.py

import sqlite3
import pandas as pd
from tabulate import tabulate

def execute_query(query):
    conn = sqlite3.connect("taif_medical.db")  # Connect to the database file
    try:
        # Split multiple SQL statements
        for stmt in query.split(";"):
            if stmt.strip():  # Execute only if the statement is not empty
                cur = conn.cursor()
                cur.execute(stmt)
                results = cur.fetchall()
                # Get column names from cursor description
                col_names = [desc[0] for desc in cur.description]
                # Display results in a table
                if results:
                  print(tabulate(results, headers=col_names, tablefmt="fancy_grid"))  # Use col_names here
                else:
                  print("No results found.")
    except Exception as e:
        print(f"Error executing SQL query: {e}")
    finally:
        conn.close()
