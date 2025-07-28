
from io import BytesIO
import pandas as pd


def get_urls(container):
    blob_name = "raw/market-urls.csv"
    blob_client = container.get_blob_client(blob=blob_name)

    data = blob_client.download_blob().readall()
    df = pd.read_csv(BytesIO(data))

    return df

def append_prices(container, ticker:str, tickerType:str, prices:list):
    print(f"Appending prices for {ticker} of type {tickerType}")
    blob_name = f"bronze/{ticker}.csv"
    blob_client = container.get_blob_client(blob=blob_name)

    data = blob_client.download_blob()
    blob_data = data.readall()
    df = pd.read_csv(BytesIO(blob_data))

    column_names = ["Date", "Open", "High", "Low", "Close", "Volume"]
    prices[0] = str(prices[0]) 

    new_df = pd.DataFrame([prices], columns=column_names)
    df = pd.concat([new_df, df], ignore_index=True)
   
    updated_blob_data = df.to_csv(index=False).encode('utf-8')
    blob_client.upload_blob(updated_blob_data, overwrite=True)

    return

def save_to_silver(container, etfPrices):
    blob_name = f"silver/etf_silver.csv"
    blob_client = container.get_blob_client(blob=blob_name)
    
    data = etfPrices.to_csv(index=False).encode('utf-8')
    blob_client.upload_blob(data, overwrite=True)
    
    

def get_list_of_files(container):
    blobs = container.list_blobs(name_starts_with="bronze/")
    csv_files = [blob.name for blob in blobs if blob.name.lower().endswith(".csv")]
    return csv_files

