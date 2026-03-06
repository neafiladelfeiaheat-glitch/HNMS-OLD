from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
from datetime import datetime
import os

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# Ξεκινάμε με ένα κανονικό πλάτος. Το ύψος θα το φτιάχνουμε δυναμικά.
chrome_options.add_argument('--window-size=1920,1080')

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')

driver = webdriver.Chrome(options=chrome_options)

regions = {
    "Attiki": "http://oldportal.emy.gr/emy/el/observation/yesterday_weather?perifereia=Attiki",
    "East_Macedonia_and_Thrace": "http://oldportal.emy.gr/emy/el/observation/yesterday_weather?perifereia=East%20Macedonia%20and%20Thrace",
    "Central_Macedonia": "http://oldportal.emy.gr/emy/el/observation/yesterday_weather?perifereia=Central%20Macedonia",
    "West_Macedonia": "http://oldportal.emy.gr/emy/el/observation/yesterday_weather?perifereia=West%20Macedonia",
    "Epirus": "http://oldportal.emy.gr/emy/el/observation/yesterday_weather?perifereia=Epirus",
    "Thessaly": "http://oldportal.emy.gr/emy/el/observation/yesterday_weather?perifereia=Thessaly",
    "Ionian_Islands": "http://oldportal.emy.gr/emy/el/observation/yesterday_weather?perifereia=Ionian%20Islands",
    "West_Greece": "http://oldportal.emy.gr/emy/el/observation/yesterday_weather?perifereia=West%20Greece",
    "Sterea": "http://oldportal.emy.gr/emy/el/observation/yesterday_weather?perifereia=Sterea",
    "Peloponnese": "http://oldportal.emy.gr/emy/el/observation/yesterday_weather?perifereia=Peloponnese",
    "North_Aegean": "http://oldportal.emy.gr/emy/el/observation/yesterday_weather?perifereia=North%20Aegean",
    "South_Aegean": "http://oldportal.emy.gr/emy/el/observation/yesterday_weather?perifereia=South%20Aegean",
    "Crete": "http://oldportal.emy.gr/emy/el/observation/yesterday_weather?perifereia=Crete"
}

all_data = []
today = datetime.now().strftime("%Y-%m-%d")
save_folder = f"screenshots/{today}"
os.makedirs(save_folder, exist_ok=True)

try:
    for region_name, url in regions.items():
        print(f"Επεξεργασία Περιφέρειας: {region_name}")
        driver.get(url)
        time.sleep(3) # Χρόνος για να φορτώσει ο πίνακας
        
        # --- ΔΥΝΑΜΙΚΟ ΜΕΓΕΘΟΣ ΟΘΟΝΗΣ ---
        # Υπολογίζουμε το πραγματικό ύψος ολόκληρης της σελίδας
        total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        # Ρυθμίζουμε το παράθυρο ακριβώς στο ύψος της σελίδας + 150 pixels αέρα
        driver.set_window_size(1920, total_height + 150)
        time.sleep(1) # Μικρή παύση για να προσαρμοστεί το παράθυρο πριν το κλικ
        
        # Τραβάμε ολόκληρη τη σελίδα
        driver.save_screenshot(f"{save_folder}/{region_name}.png")

        # --- EXCEL ΔΕΔΟΜΕΝΑ ---
        rows = driver.find_elements(By.CSS_SELECTOR, "table tr")
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if cols:
                all_data.append([today, region_name] + [c.text.strip() for c in cols])

    # Αποθήκευση στο Excel
    excel_file = 'weather_history.xlsx'
    df_new = pd.DataFrame(all_data, columns=['Ημερομηνία', 'Περιφέρεια', 'Σταθμός', 'Μέγιστη Θερμ.', 'Ελάχιστη Θερμ.', 'Βροχόπτωση'])

    if os.path.exists(excel_file):
        df_old = pd.read_excel(excel_file)
        df_final = pd.concat([df_old, df_new], ignore_index=True).drop_duplicates()
        df_final.to_excel(excel_file, index=False)
    else:
        df_new.to_excel(excel_file, index=False)
    
    print("Όλα τα links ενημερώθηκαν σωστά με το σωστό μέγεθος!")

except Exception as e:
    print(f"Σφάλμα: {e}")
finally:
    driver.quit()
