from src.utils.savetoblob import *
from datetime import datetime
from time import sleep

import os
import requests

from dotenv import load_dotenv
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


if os.path.exists('.env'):
    load_dotenv()

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080") 
    chrome_options.add_argument("--log-level=3")  # Only fatal logs
    chrome_options.add_argument("--disable-logging")  # Extra suppression
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def get_market():
    try:
        print("Fetching market URLs...")
        df = get_market_urls()
        return df
    except Exception as e:
        return None

def append_ohclv(tickerName, marketData):
    try:
        result = append_latest_ohclv(tickerName, marketData)
        if result["is_success"]:
            print(f"Successfully appended OHLCV data for {tickerName}")
        else:
            print(f"Failed to append OHLCV data for {tickerName}: {result.get('error')}")
    except Exception as e:
        print(f"Error appending OHLCV data for {tickerName}: {e}")
        return None


def extract_prices(driver, xpath):
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
    return element.text.replace('"','').strip()

def process_url(driver, url, tickerType, ticker):
    current_price = {}
    try:
        if tickerType == "stocks":
            driver.get(url)
            WebDriverWait(driver, 20).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "company_infos")))

            current_price = {
                "open": extract_prices(driver,"/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[1]/td[4]"),
                "high": extract_prices(driver,"/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[2]/td[4]"),
                "low": extract_prices(driver,"/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[3]/td[4]"),
                "close": extract_prices(driver,"/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[1]/td[6]"),
                "volume": extract_prices(driver,"/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[3]/td[2]")
            }
        print(f"Scraping successful for {ticker}")
        return current_price
    
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None
    finally:
        driver.switch_to.default_content()
        pass

def main():    
    #api = f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/"
    data = get_market()
   
    if data is None or data.empty:
        print("Failed to retrieve market URLs.")
        return
    
    for _, row in data.iterrows():
        url = row['URL']
        ticker = row['TICKER'].lower()
        tickerType = row['TYPE'].lower()
        
        print(f"Processing {ticker}")
        
        driver = init_driver()
        try:
            prices = process_url(driver, url, tickerType, ticker)
            if prices:
                prices_list = [datetime.now().strftime("%m/%d/%Y"), prices["open"], prices["high"], prices["low"], prices["close"], prices["volume"]]
                print(ticker, prices_list)
                append_ohclv(ticker, prices_list)  
        except Exception as e:
            print(f"Error scraping for {ticker}: {e}")
        finally:
            driver.quit()
        
        sleep(10)


if __name__ == "__main__":    
    main()