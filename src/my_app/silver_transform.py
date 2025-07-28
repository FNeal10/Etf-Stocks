import os
import pandas as pd
from io import StringIO
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_CONNECTION_STRING"))
container = service_client.get_container_client(os.getenv("CONTAINER_NAME"))

def clean_add_features(df: pd.DataFrame, source: str):

    df.insert(0, source)
    df["Volume"] = df["Volume"].str.replace(',','').astype(int)
    df["Date"] = pd.to_datetime(df["Date"], format='%m/%d/%Y')

    # Dates
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df["Year"] = df["Date"].dt.year
    df["DayOfWeek"] = df["Date"].dt.dayofweek

    df["MA_5"] = df["Close"].rolling(5).mean()
    df["MA_20"] = df["Close"].rolling(20).mean()
    df["EMA_5"] = df["Close"].ewm(span=5, adjust=False).mean()
    df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean()
    df["STD_5"] = df["Close"].rolling(5).mean()
    df["STD_20"] = df["Close"].rolling(20).mean()

    df["DailyReturn"] = df["Close"].pct_change()
    df["Volatility"] = df["DailyReturn"].rolling(20).std()
    df["PriceChange"] = df["Close"] - df["Open"]
 
    return df

def save_silver(data: pd.DataFrame):
    blob_name = f"silver/etf_silver.csv"
    blob_client = container.get_blob_client(blob=blob_name)
    
    data = data.to_csv(index=False).encode('utf-8')
    blob_client.upload_blob(data, overwrite=True)

def get_record():
    staging = []
    for blob in container.list_blobs(name_starts_with="bronze/bdo.csv"):
        if blob.name.endswith('.csv'):
            blob_client = container.get_blob_client(blob.name)
            content = blob_client.download_blob().readall().decode('utf-8')

            file = pd.read_csv(StringIO(content))
            staging.append(clean_add_features(file, os.path.basename(blob.name).replace('csv','')))
            
    save_silver(staging)

if __name__ == "__main__":
    get_record()