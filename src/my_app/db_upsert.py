import io
import os

from src.utils.database import load_to_staging
from src.utils.adlsblob import get_silver_data

from dotenv import load_dotenv

if os.path.exists('.env'):
    load_dotenv()
    

def main():
    silver = get_silver_data()
    if silver is not None:
        
        silver = silver.rename(columns={      
            "Source": "Ticker",               
            "Date": "TransactionDate",
            "Open": "PriceOpen",
            "High": "PriceHigh",
            "Close": "PriceClose",
            "Low": "PriceLow",
            "Volume": "PriceVolume"
        })
                
        print(silver.columns)
        print("Silver data fetched successfully.")
        
        upload_data = load_to_staging(silver)
        print(upload_data)
        
        


if __name__ == "__main__":
    main()