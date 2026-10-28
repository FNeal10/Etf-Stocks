import os
import sys
import json
import pandas as pd

import requests
import numpy as np

from io import StringIO, BytesIO
from dotenv import load_dotenv

from src.utils.adlsblob import *
from src.utils.helper import format_to_decimal

if os.path.exists('.env'):
    load_dotenv()

def clean_data(df):
    df["TransactionDate"] = pd.to_datetime(df["Date"].str.strip(), format='%m/%d/%Y')
    
    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']

    for col in numeric_columns:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(',', '', regex=False),
            errors='coerce'
    )

    df["PriceOpen"] = df["Open"].apply(format_to_decimal).astype(float)
    df["PriceHigh"] = df["High"].apply(format_to_decimal).astype(float)
    df["PriceClose"] = df["Close"].apply(format_to_decimal).astype(float)
    df["PriceLow"] = df["Low"].apply(format_to_decimal).astype(float)
    df["PriceVolume"] = df["Volume"].astype("Int64")
    return df

def add_features(df, source=None):

    # Sort by date
    df = df.sort_values(by="TransactionDate").reset_index(drop=True)
    df.insert(0, "Ticker", source)

    # ------------------- Date/Time Features -------------------
    df['Year'] = df['TransactionDate'].dt.year
    df['Month'] = df['TransactionDate'].dt.month
    df['Day'] = df['TransactionDate'].dt.day
    df['DayOfWeek'] = df['TransactionDate'].dt.dayofweek
    df['DayOfYear'] = df['TransactionDate'].dt.dayofyear
    df['WeekOfYear'] = df['TransactionDate'].dt.isocalendar().week
    df['Quarter'] = df['TransactionDate'].dt.quarter
    df['IsMonthStart'] = df['TransactionDate'].dt.is_month_start
    df['IsMonthEnd'] = df['TransactionDate'].dt.is_month_end
    df['IsQuarterStart'] = df['TransactionDate'].dt.is_quarter_start
    df['IsQuarterEnd'] = df['TransactionDate'].dt.is_quarter_end

    # ------------------- Price-Based Features -------------------
    df['PriceChange'] = df['PriceClose'] - df['PriceOpen']
    df['HighLowRange'] = df['PriceHigh'] - df['PriceLow']
    df['CloseOpenRange'] = df['PriceClose'] - df['PriceOpen']
    df['PercentChange'] = (df['PriceClose'] - df['PriceOpen']) / df['PriceOpen']

    # ------------------- Moving Averages -------------------
    windows = [5, 10, 20, 50, 100, 200]
    for w in windows:
        df[f"SMA_{w}"] = df['PriceClose'].rolling(window=w).mean()
        df[f"EMA_{w}"] = df['PriceClose'].ewm(span=w, adjust=False).mean()

    # ------------------- Volatility -------------------
    df['Volatility_20'] = df['Close'].pct_change().rolling(window=20).std()

    # ------------------- Momentum Indicators -------------------
    # RSI
    delta = df['PriceClose'].diff()
    gain = delta.clip(lower=0).rolling(window=14).mean()
    loss = -delta.clip(upper=0).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD
    df['EMA_12'] = df['PriceClose'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['PriceClose'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # ------------------- ADX & DI -------------------
    # True Range
    df['TR'] = np.maximum(df['PriceHigh'] - df['PriceLow'], 
                          np.maximum(abs(df['PriceHigh'] - df['PriceClose'].shift()), abs(df['PriceLow'] - df['PriceClose'].shift())))
    
    # Directional Movement
    df['+DM'] = df['High'].diff().clip(lower=0)
    df['-DM'] = -df['Low'].diff().clip(upper=0)

    # Smooth
    tr14 = df['TR'].rolling(14).sum()
    plus_dm14 = df['+DM'].rolling(14).sum()
    minus_dm14 = df['-DM'].rolling(14).sum()
    df['PlusDI'] = 100 * (plus_dm14 / tr14)
    df['MinusDI'] = 100 * (minus_dm14 / tr14)
    df['ADX'] = abs(df['PlusDI'] - df['MinusDI']).rolling(14).mean()

    # ------------------- Parabolic SAR -------------------
    df['SAR'] = df['PriceClose'].rolling(2).mean()  

    # ------------------- Volume -------------------
    df['Volume_20'] = df['PriceVolume'].rolling(20).mean()
    df['Volume_50'] = df['PriceVolume'].rolling(50).mean()

    # ------------------- Bollinger Bands -------------------
    df['BB_Middle'] = df['SMA_20']
    df['BB_Upper'] = df['BB_Middle'] + (df['PriceClose'].rolling(20).std() * 2)
    df['BB_Lower'] = df['BB_Middle'] - (df['PriceClose'].rolling(20).std() * 2)

    # ------------------- Stochastic Oscillator -------------------
    low_min = df['PriceLow'].rolling(14).min()
    high_max = df['PriceHigh'].rolling(14).max()
    df['Stochastic'] = ((df['PriceClose'] - low_min) / (high_max - low_min)) * 100

    # ------------------- Commodity Channel Index -------------------
    df['CCI'] = (df['PriceClose'] - df['SMA_20']) / (0.015 * (df['PriceHigh'] - df['PriceLow']).rolling(20).mean())

    # Drop helper columns
    df.drop(
    columns=[
        'TR', '+DM', '-DM',
        'Date', 'Open', 'High', 'Low', 'Close', 'Volume'
    ],
    errors='ignore',
    inplace=True
)

    return df


def get_bronze():
    try:
        bronze = get_bronze_files()
        return bronze
    except Exception as e:
        print(f"Error fetching bronze files: {e}")
        return []

def get_data_contents(file_name):
    try:
        data = get_file_data(file_name)
        return pd.read_csv(StringIO(data))
    except Exception as e:
        print(f"Error fetching data contents: {e}")
        return pd.DataFrame()

def upload_silver(df, ticker):
    try:
        result = create_silver_file(df, ticker)
        if result["is_success"]:
            print(f"Successfully created silver data for {ticker}")
        else:
            print(f"Failed to create silver data for {ticker}: {result.get('error')}")
    except Exception as e:
        print(f"Error uploading silver file: {e}")

def main():
    #api = f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/"

    print(f"Getting bronze files...")
    bronze_data = get_bronze()
    if bronze_data:
        for data in bronze_data:
            print(data)
            
            tickername = data.replace(".csv","").replace("bronze/","")
            print(f"Processing {data}...")
            contents = get_data_contents(data.replace("bronze/",""))
            print(f"Contents generated for {data}...")
            if not contents.empty:
                df_cleaned = clean_data(contents)
                df_cleaned = add_features(df_cleaned, tickername)
                print(f"Cleaned and added features for {data}... Uploading to blob storage.")
                upload_silver(df_cleaned, tickername)
    else:
        pass

if __name__ == "__main__":
    main()