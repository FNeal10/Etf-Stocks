import os
import sys
import pandas as pd
import requests

from io import StringIO
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

from src.utils.helper import format_to_decimal

if os.path.exists('.env'):
    load_dotenv()

def clean_data(df):
    df["Volume"] = df["Volume"].str.replace(',','').replace("'","").replace(".","").astype(int)
    df["Date"] = pd.to_datetime(df["Date"], format='%m/%d/%Y')

    df["Open"] = df["Open"].apply(format_to_decimal).astype(float)
    df["High"] = df["High"].apply(format_to_decimal).astype(float)
    df["Close"] = df["Close"].apply(format_to_decimal).astype(float)
    df["Low"] = df["Low"].apply(format_to_decimal).astype(float)
    return df

def add_features(df: pd.DataFrame, source: str):

    df.insert(0, "Source", source)    

    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df["Year"] = df["Date"].dt.year
    df["DayOfWeek"] = df["Date"].dt.dayofweek
    df["Quarter"] = df["Date"].dt.quarter
    df["IsMonthStart"] = df["Date"].dt.is_month_start.astype(bool)
    df["IsMonthEnd"] = df["Date"].dt.is_month_end.astype(bool)
    df["IsQuarterStart"] = df["Date"].dt.is_quarter_start.astype(bool)
    df["IsQuarterEnd"] = df["Date"].dt.is_quarter_end.astype(bool)
    df["DayOfyear"] = df["Date"].dt.dayofyear

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
    df.to_csv(csv_buffer, index=False, encoding='utf-8', na_rep='nan')
    csv_buffer.seek(0)

    blob_client = serviceClient.get_blob_client(container=containerName, blob=blobName)
    blob_client.upload_blob(csv_buffer.getvalue(), overwrite=True)

def append_latest_to_silver(df, serviceClient, containerName, blobName):
    try:
        blob_client = serviceClient.get_blob_client(container=containerName, blob=blobName)
        existing_data = blob_client.download_blob().readall().decode('utf-8')
        existing_df = pd.read_csv(StringIO(existing_data), parse_dates=["Date"], keep_default_na=True, na_values=['nan', 'NaN'])

        df = pd.concat([existing_df, df], ignore_index=True)
        df = df.replace('',pd.NA)
    except Exception as e:
        print(f"Error reading existing data: {e}")

    upload_silver_to_blob(df, serviceClient, containerName, blobName)


def main():

    

    #combinedData = pd.DataFrame() # STAGING DATAFAME TO HANDLE FILES

    # for blob in blobContainer.list_blobs(name_starts_with=f"{bronzeLocation}"):

    #     blob_client = blobContainer.get_blob_client(blob.name)
    #     stockPrices = blob_client.download_blob().readall().decode('utf-8')

    #     data = pd.read_csv(StringIO(stockPrices), keep_default_na=True, parse_dates=["Date"])

    #     data = data.head(1)
    #     data = clean_data(data)
    #     data = add_features(data, os.path.basename(blob.name).replace('.csv',''))

    #     combinedData = pd.concat([combinedData, data], ignore_index=True)

    # #upload_silver_to_blob(combinedData, serviceClient, os.getenv("CONTAINER_NAME"), f"{silverFile}silver_output.csv")
    # append_latest_to_silver(combinedData, serviceClient, os.getenv("CONTAINER_NAME"), f"{silverFile}silver_output.csv")
    # return combinedData, data

if __name__ == "__main__":
    main()