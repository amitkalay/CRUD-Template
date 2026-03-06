import pandas as pd
import sqlite3

# 1. Load the data
df = pd.read_csv("data.csv")

# 2. Connect to (or create) the database file — with closes it automatically
with sqlite3.connect("assignment.db") as conn:
    # 3. Write to SQLite
    # 'if_exists=replace' creates the table if it's missing or overwrites it
    df.to_sql("my_table", conn, if_exists="replace", index=False)

print("Done! Data migrated to SQLite.")
