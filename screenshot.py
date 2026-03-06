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

# Η "ΜΕΤΑΜΦΙΕΣΗ": Λέμε στον server ότι είμαστε κανονικός Chrome σε Windows
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')

driver = webdriver.Chrome(options=chrome_options)

# Προσθέτουμε extra headers για να φαινόμαστε πιο αληθινοί
url = "http://oldportal.emy.gr/emy/el/observation/yesterday_weather?perifereia=Attiki"

try:
    print("Προσπάθεια σύνδεσης...")
    driver.get(url)
    
    # Περιμένουμε λίγο παραπάνω για να "ηρεμήσει" το firewall
    time.sleep(10) 

    os.makedirs('screenshots', exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"screenshots/emy_weather_{date_str}.png"

    driver.save_screenshot(filename)
    print("Το screenshot σώθηκε επιτυχώς!")
except Exception as e:
    print(f"Σφάλμα: {e}")
finally:
    driver.quit()
