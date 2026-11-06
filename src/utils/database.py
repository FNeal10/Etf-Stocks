import os
import time
import pyodbc
import pandas as pd
from dotenv import load_dotenv


# Load environment variables
load_dotenv(override=True)



def connect_to_azure_sql(connectionString, retries=5, timeout=120):

    for attempt in range(1, retries + 1):
        try:
            print(f"Connecting to Azure SQL... Attempt {attempt}/{retries}")

            connection = pyodbc.connect(
                connectionString,
                timeout=timeout,
                autocommit=False
            )

            print("Connected to Azure SQL Database.")
            return connection

        except pyodbc.Error as e:
            print(f"Attempt {attempt} failed: {e}")

            if attempt == retries:
                raise

            wait_time = 30
            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    
def load_to_staging(df, server_type=1):
    """
    Load Silver data into Azure SQL staging, execute the upsert
    procedure, and commit the entire operation once.

    1 = Azure SQL Server
    2 = Local SQL Server
    
    Returns:
        bool: True if successful, False otherwise.
    """

    if df is None or df.empty:
        print("No data to load.")
        return True

    connection = None

    try:
       
        if server_type == 1:
            print("Connecting to AZURE SQL Database...")
            staging_table_sql = os.getenv('DB_AZURE_STAGING_TABLE_NAME')
            connection_string = (
                "DRIVER={ODBC Driver 18 for SQL Server};"
                f"SERVER=tcp:{os.getenv('DB_AZURE_SERVER')},1433;"
                f"DATABASE={os.getenv('DB_AZURE_DATABASE')};"
                f"UID={os.getenv('DB_AZURE_USERNAME')};"
                f"PWD={os.getenv('DB_AZURE_PASSWORD')};"
                "Encrypt=yes;"
                "TrustServerCertificate=no;"
            )

            connection = connect_to_azure_sql(
                connection_string,
                retries=5,
                timeout=120
            )
            
        else: # SQL LOCAL
            print("Connecting to LOCAL SQL Database...")
            staging_table_sql = os.getenv('DB_LOCAL_STAGING_TABLE_NAME')
            connection = pyodbc.connect(
                "DRIVER={ODBC Driver 18 for SQL Server};"
                f"SERVER={os.getenv('DB_LOCAL_SERVER')};"
                f"DATABASE={os.getenv('DB_LOCAL_DATABASE')};"
                f"UID={os.getenv('DB_LOCAL_USERNAME')};"
                f"PWD={os.getenv('DB_LOCAL_PASSWORD')};"
                "Encrypt=yes;"
                "TrustServerCertificate=yes;"
                "Connection Timeout=30;",
                autocommit=False,
            )

        cursor = connection.cursor()

        # Convert pandas NaN/NaT values to Python None
        clean_df = df.astype(object).where(df.notna(), None)

        # Build INSERT statement
        columns = list(clean_df.columns)
        column_sql = ", ".join(
            f"[{col}]" for col in columns
        )
        placeholders = ", ".join(
            "?" for _ in columns
        )

        insert_sql = f"""
            INSERT INTO {staging_table_sql}
            ({column_sql})
            VALUES ({placeholders})
        """

        # Insert rows in batches without committing
        cursor.fast_executemany = True
        batch_size = 1000

        print(f"Loading {len(clean_df)} rows into staging...")

        for start in range(0, len(clean_df), batch_size):
            batch = clean_df.iloc[start:start + batch_size]

            cursor.executemany(
                insert_sql,
                list(batch.itertuples(index=False, name=None)),
            )

            print(
                f"Processed {min(start + len(batch), len(clean_df))}"
                f" of {len(clean_df)} rows."
            )

        # Execute the transaction-aware stored procedure.
        # It must not commit the caller-owned transaction.
        print("Executing dbo.spUpsert_MarketData...")

        cursor.execute("EXEC dbo.spUpsert_MarketData;")

        # Read the procedure's result set
        result = None

        while True:
            if cursor.description is not None:
                result = cursor.fetchone()
                break

            if not cursor.nextset():
                break

        if result is not None:
            print("Upsert results:")
            print(f"  Updated rows: {result[0]}")
            print(f"  Inserted rows: {result[1]}")
        else:
            raise RuntimeError(
                "The stored procedure did not return row counts."
            )

        # The single commit for both staging inserts and the upsert
        connection.commit()

        print("Transaction committed successfully.")
        return True

    except Exception as e:
        if connection is not None:
            try:
                connection.rollback()
                print("Transaction rolled back.")
            except pyodbc.Error as rollback_error:
                print(f"Rollback error: {rollback_error}")

        print(f"Error loading data: {e}")
        return False

    finally:
        if connection is not None:
            connection.close()
            print("Database connection closed.")


