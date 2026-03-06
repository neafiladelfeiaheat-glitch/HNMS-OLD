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

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')

driver = webdriver.Chrome(options=chrome_options)

# Η λίστα με όλες τις περιφέρειες που ζήτησες
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
# Φτιάχνουμε φάκελο με τη σημερινή ημερομηνία για να είναι οργανωμένα τα 13 screenshots
save_folder = f"screenshots/{today}"
os.makedirs(save_folder, exist_ok=True)

try:
    for region_name, url in regions.items():
        print(f"Επεξεργασία Περιφέρειας: {region_name}")
        driver.get(url)
        time.sleep(4) # Το παλιό site είναι γρήγορο, δεν χρειάζεται 15 δεύτερα
        
        # --- ΤΕΛΕΙΟ SCREENSHOT (Μόνο ο πίνακας) ---
        # Βρίσκουμε τον πίνακα και φωτογραφίζουμε μόνο αυτό το στοιχείο (κομμένο και ραμμένο)
        try:
            table_element = driver.find_element(By.CSS_SELECTOR, "table.table")
            table_element.screenshot(f"{save_folder}/{region_name}.png")
        except:
            # Αν κάτι πάει στραβά, παίρνει όλη την οθόνη αλλά τη φέρνει στα μέτρα του body
            width = driver.execute_script("return document.body.scrollWidth")
            height = driver.execute_script("return document.body.scrollHeight")
            driver.set_window_size(width, height)
            driver.save_screenshot(f"{save_folder}/{region_name}.png")

        # --- EXCEL ΔΕΔΟΜΕΝΑ ---
        rows = driver.find_elements(By.CSS_SELECTOR, "table tr")
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if cols:
                # Προσθέτουμε την Ημερομηνία ΚΑΙ την Περιφέρεια στην αρχή
                all_data.append([today, region_name] + [c.text.strip() for c in cols])

    # Αποθήκευση όλων των δεδομένων στο Excel
    excel_file = 'weather_history.xlsx'
    # Προσθέσαμε τη στήλη 'Περιφέρεια' για να ξεχωρίζουν
    df_new = pd.DataFrame(all_data, columns=['Ημερομηνία', 'Περιφέρεια', 'Σταθμός', 'Μέγιστη Θερμ.', 'Ελάχιστη Θερμ.', 'Βροχόπτωση'])

    if os.path.exists(excel_file):
        df_old = pd.read_excel(excel_file)
        df_final = pd.concat([df_old, df_new], ignore_index=True).drop_duplicates()
        df_final.to_excel(excel_file, index=False)
    else:
        df_new.to_excel(excel_file, index=False)
    
    print("Όλα τα links ενημερώθηκαν σωστά!")

except Exception as e:
    print(f"Σφάλμα: {e}")
finally:
    driver.quit()
