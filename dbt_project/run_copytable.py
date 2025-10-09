import os
import duckdb as ddb

from dotenv import load_dotenv

load_dotenv()


def create_table():
    gold_parquet = os.getenv("GOLD_PARQUET") 
    
    con = ddb.connect("dev.duckdb")

    con.execute(f"""
        CREATE OR REPLACE TABLE tblStocks AS
        SELECT * FROM read_parquet('{gold_parquet}');
    """)

    con.close()
    
if __name__ == "__main__":
    create_table()