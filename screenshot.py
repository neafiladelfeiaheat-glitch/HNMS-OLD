from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
from datetime import datetime
import os

# Ρυθμίσεις Browser
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')

driver = webdriver.Chrome(options=chrome_options)
url = "http://oldportal.emy.gr/emy/el/observation/yesterday_weather?perifereia=Attiki"

try:
    driver.get(url)
    time.sleep(10) # Αναμονή για το φόρτωμα

    # 1. Screenshot
    os.makedirs('screenshots', exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    driver.save_screenshot(f"screenshots/emy_weather_{today}.png")

    # 2. Διάβασμα Πίνακα
    rows = driver.find_elements(By.CSS_SELECTOR, "table tr")
    new_data = []
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if cols:
            new_data.append([today] + [c.text.strip() for c in cols])

    # 3. Αποθήκευση σε Excel (.xlsx)
    excel_file = 'weather_history.xlsx'
    columns = ['Ημερομηνία', 'Σταθμός', 'Μέγιστη Θερμ.', 'Ελάχιστη Θερμ.', 'Βροχόπτωση']
    df_new = pd.DataFrame(new_data, columns=columns)

    if os.path.exists(excel_file):
        df_old = pd.read_excel(excel_file)
        df_final = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_final = df_new

    df_final.to_excel(excel_file, index=False)
    print("Το Excel ενημερώθηκε!")

except Exception as e:
    print(f"Σφάλμα: {e}")
finally:
    driver.quit()
