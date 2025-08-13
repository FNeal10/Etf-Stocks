
from io import BytesIO
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from dotenv import load_dotenv

from datetime import datetime
import pandas as pd
import os

load_dotenv()

service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_CONNECTION_STRING"))
container_client = service_client.get_container_client(os.getenv("CONTAINER_NAME"))

bronze_path = os.getenv("BRONZE_LOCATION")
silver_path = os.getenv("SILVER_LOCATION")

def get_market_urls():
    """
    Fetches market URLs from the Azure Blob Storage.
    :return: DataFrame containing market URLs.
    """
    blob_name = "raw/market-urls.csv"
    blob_client = container_client.get_blob_client(blob=blob_name)

    try:
        data = blob_client.download_blob().readall()
        df = pd.read_csv(BytesIO(data))
        return df
    except (ResourceNotFoundError, ResourceExistsError):
        return None
    except Exception as e:
        return None

def append_latest_ohclv(ticker_name, market_data:list):
    """
    Appends the latest OHLCV data to the specified blob in Azure Blob Storage.
    :param tickerName: Name of the ticker.
    :param tickerType: Type of the ticker (e.g., stock, ETF).
    :param priceInfo: List containing the OHLCV price information.
    :return: None
    """
    blob_name = f"{bronze_path}{ticker_name}.csv"
    blob_client = container_client.get_blob_client(blob=blob_name)
    blob_data = blob_client.download_blob().readall()
    existing_data = pd.read_csv(BytesIO(blob_data))

    column_names = ["Date", "Open", "High", "Low", "Close", "Volume"]
    market_data[0] = str(market_data[0])
    latest_data = pd.DataFrame([market_data], columns=column_names)
    
    data = pd.concat([latest_data, existing_data], ignore_index=True)
    blob_data = data.to_csv(index=False).encode('utf-8')

    try:
        blob_client.upload_blob(blob_data, overwrite=True)
        return {"is_success": True, "message": "Data appended successfully"}
    except Exception as e:
        return {"is_success": False, "message": str(e)}

def get_bronze_files():
    """
    Fetches all bronze files from the Azure Blob Storage.
    :return: List of bronze file names.
    """
    blobs = container_client.list_blobs(name_starts_with="bronze/")
    bronze_files = [blob.name for blob in blobs if blob.name.lower().endswith(".csv")]
    return bronze_files

def get_file_data(file_name):
    """
    Fetches data from a specific file in Azure Blob Storage.
    :param file_name: Name of the file to fetch data from.
    :return: DataFrame containing the file data.
    """
    blob_name = f"{bronze_path}{file_name}"
    blob_client = container_client.get_blob_client(blob=blob_name)

    try:
        data = blob_client.download_blob().readall()
        csv_string = data.decode('utf-8')
        return csv_string
    except ResourceNotFoundError:
        return None
    except Exception as e:
        return None

def create_silver_file(silver_file):
    """
    Creates a silver file from the provided parquet file.
    :param parquet_file: Parquet file data.
    :return: None
    """
    blob_name = f"{silver_path}{datetime.now().strftime('%Y-%m%d')}.csv"
    blob_client = container_client.get_blob_client(blob=blob_name)

    try:
        blob_client.upload_blob(silver_file, overwrite=True)
        return {"is_success": True, "message": "Silver file created successfully"}
    except Exception as e:
        return {"is_success": False, "message": str(e)}
    
