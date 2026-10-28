
import os
import pyodbc
import pandas as pd
from dotenv import load_dotenv


# Load environment variables
load_dotenv(override=True)


def load_to_staging(df):
    """
    Load Silver data into Azure SQL staging, execute the upsert
    procedure, and commit the entire operation once.

    Returns:
        bool: True if successful, False otherwise.
    """

    if df is None or df.empty:
        print("No data to load.")
        return True

    # Validate required environment variables
    required_variables = [
        "DB_AZURE_SERVER",
        "DB_AZURE_DATABASE",
        "DB_AZURE_USERNAME",
        "DB_AZURE_PASSWORD",
        "DB_AZURE_STAGING_TABLE_NAME",
    ]

    missing_variables = [
        name for name in required_variables
        if not os.getenv(name)
    ]

    if missing_variables:
        print(
            "Missing environment variables: "
            + ", ".join(missing_variables)
        )
        return False

    staging_table = os.getenv("DB_AZURE_STAGING_TABLE_NAME")

    # Prevent SQL identifier injection through the table setting.
    # Expected format: dbo.marketprices_staging
    table_parts = staging_table.split(".")

    if (
        len(table_parts) != 2
        or not all(
            part.replace("_", "").isalnum()
            for part in table_parts
        )
    ):
        print(
            "Invalid staging table name. "
            "Use a schema-qualified name such as "
            "dbo.marketprices_staging."
        )
        return False

    staging_table_sql = ".".join(
        f"[{part}]" for part in table_parts
    )

    connection = None

    try:
        print("Connecting to Azure SQL Database...")

        connection = pyodbc.connect(
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER=tcp:{os.getenv('DB_AZURE_SERVER')},1433;"
            f"DATABASE={os.getenv('DB_AZURE_DATABASE')};"
            f"UID={os.getenv('DB_AZURE_USERNAME')};"
            f"PWD={os.getenv('DB_AZURE_PASSWORD')};"
            "Encrypt=yes;"
            "TrustServerCertificate=no;"
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
            VALUES ({placeholders});
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


