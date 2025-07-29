import os
import sys
import pandas as pd
from io import StringIO
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

from src.utils.helper import format_to_decimal, append_to_log

def clean_and_add_features(df: pd.DataFrame, source: str):

    df.insert(0, "Source", source)
    df["Volume"] = df["Volume"].str.replace(',','').replace("'","").replace(".","").astype(int)
    df["Date"] = pd.to_datetime(df["Date"], format='%m/%d/%Y')
    
    df["Open"] = df["Open"].apply(format_to_decimal).astype(float)
    df["High"] = df["High"].apply(format_to_decimal).astype(float)
    df["Close"] = df["Close"].apply(format_to_decimal).astype(float)
    df["Low"] = df["Low"].apply(format_to_decimal).astype(float)

    # Dates
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df["Year"] = df["Date"].dt.year
    df["DayOfWeek"] = df["Date"].dt.dayofweek

    df["MA_5"] = df["Close"].rolling(5).mean().apply(format_to_decimal)
    df["MA_20"] = df["Close"].rolling(20).mean().apply(format_to_decimal)
    df["EMA_5"] = df["Close"].ewm(span=5, adjust=False).mean().apply(format_to_decimal)
    df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean().apply(format_to_decimal)
    df["STD_5"] = df["Close"].rolling(5).mean().apply(format_to_decimal)
    df["STD_20"] = df["Close"].rolling(20).mean().apply(format_to_decimal)

    df["DailyReturn"] = df["Close"].pct_change().apply(format_to_decimal)
    df["Volatility"] = df["DailyReturn"].rolling(20).std().apply(format_to_decimal)
    df["PriceChange"] = (df["Close"] - df["Open"]).apply(format_to_decimal)
 
    return df

def upload_silver_to_blob(df, serviceClient, containerName, blobName):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    #blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_CONNECTION_STRING"))
    blob_client = serviceClient.get_blob_client(container=containerName, blob=blobName)

    blob_client.upload_blob(csv_buffer.getvalue(), overwrite=True)

def main():
    
    load_dotenv()
    combined_df = pd.DataFrame()
    serviceClient = BlobServiceClient.from_connection_string(os.getenv("AZURE_CONNECTION_STRING"))
    blobContainer = serviceClient.get_container_client(os.getenv("CONTAINER_NAME"))

    bronzeLocation = os.getenv("BRONZE_LOCATION")
    silverFileOutput = os.getenv("SILVER_OUTPUT")
   
    for blob in blobContainer.list_blobs(name_starts_with=f"{bronzeLocation}"):
        print(blob.name)
        blob_client = blobContainer.get_blob_client(blob.name)
        content = blob_client.download_blob().readall().decode('utf-8')

        file = pd.read_csv(StringIO(content))
        final = clean_and_add_features(file.head(1), os.path.basename(blob.name).replace('.csv',''))

        combined_df = pd.concat([combined_df, final], ignore_index=True)
    upload_silver_to_blob(combined_df, serviceClient, os.getenv("CONTAINER_NAME"), f"{silverFileOutput}silver_output.csv")
    return combined_df


if __name__ == "__main__":
    main()