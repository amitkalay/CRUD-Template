import pandas as pd
import sqlite3

# 1. Load the data
df = pd.read_csv("UN_SYB63_314_202009_Internet_Usage - Sheet1.csv")

# 2. Connect to (or create) the database file — with closes it automatically
with sqlite3.connect("internet_usage.db") as conn:
    # 3. Write to SQLite
    # 'if_exists=replace' creates the table if it's missing or overwrites it
    df.index.name = 'id'  # Set the index name to 'id' for auto-incrementing primary key
    df.to_sql("usage_table", conn, if_exists="replace", index=True)
    df_debug = pd.read_sql_query("SELECT * FROM usage_table", conn)
    print("Column Names:", df_debug.columns.tolist())
    # print(df_debug.to_string())

print("Done! Data migrated to SQLite.")
