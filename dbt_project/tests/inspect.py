import duckdb
import os

# Absolute path to your dev.duckdb file
db_path = os.path.abspath("dev.duckdb")
print("Using database:", db_path)

con = duckdb.connect(db_path)

# List all tables to see what exists
tables = con.execute("SHOW TABLES").fetchall()
print("Tables in DB:", tables)

# Now query the table
results = con.execute("SELECT * FROM my_first_dbt_model").fetchall()
print(results)
