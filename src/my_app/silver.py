import os
import sys
import pandas as pd

import requests
import numpy as np

from io import StringIO, BytesIO
from dotenv import load_dotenv

from src.utils.helper import format_to_decimal

if os.path.exists('.env'):
    load_dotenv()

def clean_data(df):
    df["Date"] = pd.to_datetime(df["Date"], format='%m/%d/%Y')

    df["Open"] = df["Open"].apply(format_to_decimal).astype(float)
    df["High"] = df["High"].apply(format_to_decimal).astype(float)
    df["Close"] = df["Close"].apply(format_to_decimal).astype(float)
    df["Low"] = df["Low"].apply(format_to_decimal).astype(float)
    df["Volume"] = df["Volume"].str.replace(r'\D', '', regex=True).astype(int)
    return df

def add_features(df, source=None):

    # Sort by date
    df = df.sort_values(by="Date").reset_index(drop=True)
    df.insert(0, "Source", source)

    # ------------------- Date/Time Features -------------------
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['DayOfYear'] = df['Date'].dt.dayofyear
    df['WeekOfYear'] = df['Date'].dt.isocalendar().week
    df['Quarter'] = df['Date'].dt.quarter
    df['IsMonthStart'] = df['Date'].dt.is_month_start
    df['IsMonthEnd'] = df['Date'].dt.is_month_end
    df['IsQuarterStart'] = df['Date'].dt.is_quarter_start
    df['IsQuarterEnd'] = df['Date'].dt.is_quarter_end

    # ------------------- Price-Based Features -------------------
    df['PriceChange'] = df['Close'] - df['Open']
    df['HighLowRange'] = df['High'] - df['Low']
    df['CloseOpenRange'] = df['Close'] - df['Open']
    df['PercentChange'] = (df['Close'] - df['Open']) / df['Open']

    # ------------------- Moving Averages -------------------
    windows = [5, 10, 20, 50, 100, 200]
    for w in windows:
        df[f"SMA_{w}"] = df['Close'].rolling(window=w).mean()
        df[f"EMA_{w}"] = df['Close'].ewm(span=w, adjust=False).mean()

    # ------------------- Volatility -------------------
    df['Volatility_20'] = df['Close'].pct_change().rolling(window=20).std()

    # ------------------- Momentum Indicators -------------------
    # RSI
    delta = df['Close'].diff()
    gain = delta.clip(lower=0).rolling(window=14).mean()
    loss = -delta.clip(upper=0).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # ------------------- ADX & DI -------------------
    # True Range
    df['TR'] = np.maximum(df['High'] - df['Low'], 
                          np.maximum(abs(df['High'] - df['Close'].shift()), abs(df['Low'] - df['Close'].shift())))
    
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
    df['SAR'] = df['Close'].rolling(2).mean()  

    # ------------------- Volume -------------------
    df['Volume_20'] = df['Volume'].rolling(20).mean()
    df['Volume_50'] = df['Volume'].rolling(50).mean()

    # ------------------- Bollinger Bands -------------------
    df['BB_Middle'] = df['SMA_20']
    df['BB_Upper'] = df['BB_Middle'] + (df['Close'].rolling(20).std() * 2)
    df['BB_Lower'] = df['BB_Middle'] - (df['Close'].rolling(20).std() * 2)

    # ------------------- Stochastic Oscillator -------------------
    low_min = df['Low'].rolling(14).min()
    high_max = df['High'].rolling(14).max()
    df['Stochastic'] = ((df['Close'] - low_min) / (high_max - low_min)) * 100

    # ------------------- Commodity Channel Index -------------------
    df['CCI'] = (df['Close'] - df['SMA_20']) / (0.015 * (df['High'] - df['Low']).rolling(20).mean())

    # Drop helper columns
    df.drop(['TR', '+DM', '-DM'], axis=1, inplace=True)

    return df


def get_bronze_files(api):
    try:
        response = requests.post(f"{api}get-bronze")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching bronze files: {e}")
        return []

def get_data_contents(api, file_name):
    payload = {
        "file": file_name
    }
    try:
        response = requests.post(f"{api}get-file", json=payload)
        response.raise_for_status()
        return pd.read_csv(StringIO(response.text))
    except Exception as e:
        print(f"Error fetching data contents: {e}")
        return pd.DataFrame()

def upload_silver(api, df, ticker):
    try:
        payload = {
            "file": df.to_csv(index=False),
            "ticker": ticker
        }
        response = requests.post(f"{api}/create-silver", json=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Error uploading silver file: {e}")

def main():
    api = f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/"

    print(f"Getting bronze files...")
    bronze_data = get_bronze_files(api)
    if bronze_data:
        for data in bronze_data:
            tickername = data.replace(".csv","").replace("bronze/","")
            print(f"Processing {data}...")
            contents = get_data_contents(api, data.replace("bronze/",""))
            if not contents.empty:
                df_cleaned = clean_data(contents)
                df_cleaned = add_features(df_cleaned, tickername)
                upload_silver(api, df_cleaned, tickername)
    else:
        pass

if __name__ == "__main__":
    main()