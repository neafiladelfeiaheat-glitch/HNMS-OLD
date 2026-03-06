from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import os

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=chrome_options)
url = "http://oldportal.emy.gr/emy/el/observation/yesterday_weather?perifereia=Attiki"

driver.get(url)
time.sleep(5)

os.makedirs('screenshots', exist_ok=True)
date_str = datetime.now().strftime("%Y-%m-%d")
filename = f"screenshots/emy_weather_{date_str}.png"

driver.save_screenshot(filename)
driver.quit()
