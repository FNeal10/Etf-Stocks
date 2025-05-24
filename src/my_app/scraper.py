from datetime import datetime
from time import sleep
import os

from dotenv import load_dotenv
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from azure.storage.blob import BlobServiceClient

from src.data.blob_utils import get_urls, append_prices

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080") 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def extract_prices(driver, xpath):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    print(element.text)
    return element.text.replace('"','').strip()

def process_url(driver, url):
    current_price = {}
    try:
        if 'www.pse.com' in url:
            driver.get(url)
            iFrame = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "company_infos")))
            driver.switch_to.frame(iFrame)

            current_price = {
                "open": extract_prices(driver,"/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[1]/td[4]"),
                "high": extract_prices(driver,"/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[2]/td[4]"),
                "low": extract_prices(driver,"/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[3]/td[4]"),
                "close": extract_prices(driver,"/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[1]/td[6]"),
                "volume": extract_prices(driver,"/html/body/div/div/div/div[3]/div[1]/div/div[3]/table/tbody/tr[3]/td[2]")
            }
        
        return current_price
    
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None

def main():    
    load_dotenv()
    
    driver = init_driver()

    service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_CONNECTION_STRING"))
    container_client = service_client.get_container_client(os.getenv("CONTAINER_NAME"))

    data = get_urls(container_client)
    for _, row in data.iterrows():
        url = row['URL']
        ticker = row['TICKER'].lower()
        tickerType = row['TYPE']
        
        prices = process_url(driver, url)
        if prices:
            prices_list = [datetime.now().strftime("%m/%d/%Y"), prices["open"], prices["high"], prices["low"], prices["close"], prices["volume"]]
            append_prices(container_client, ticker, tickerType, prices_list)

        sleep(5)

    driver.quit()

if __name__ == "__main__":    
    main()