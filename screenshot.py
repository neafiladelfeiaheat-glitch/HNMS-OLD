from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import os

# 1. Βασικές Ρυθμίσεις Browser (κρατάμε τη μεταμφίεση)
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Η μεταμφίεση που δούλεψε!
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')

# 2. Ξεκινάμε τον driver
driver = webdriver.Chrome(options=chrome_options)
url = "http://oldportal.emy.gr/emy/el/observation/yesterday_weather?perifereia=Attiki"

try:
    print("Γίνεται φόρτωση της σελίδας...")
    driver.get(url)

    # 3. Περιμένουμε αρκετά (10 δευτ.) για να φορτώσει ολόκληρος ο πίνακας
    time.sleep(10) 

    print("Υπολογισμός μεγέθους σελίδας...")
    
    # 4. *** Η ΝΕΑ ΔΙΟΡΘΩΣΗ: "Έξυπνο" Full Page Screenshot ***
    # Ρωτάμε τη σελίδα μέσω JavaScript: "Πόσο ψηλή είσαι;"
    total_height = driver.execute_script("return document.body.scrollHeight")
    
    # Αλλάζουμε το μέγεθος του παραθύρου για να χωρέσει όλο το περιεχόμενο
    # (κρατάμε το πλάτος σταθερό στα 1920)
    driver.set_window_size(1920, total_height)
    
    # Δίνουμε 1 δευτερόλεπτο στον Chrome να προσαρμοστεί
    time.sleep(1)

    # 5. Αποθήκευση
    os.makedirs('screenshots', exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"screenshots/emy_weather_{date_str}.png"

    # 6. Λήψη του FULL screenshot
    driver.save_screenshot(filename)
    print(f"Επιτυχία! Το full screenshot αποθηκεύτηκε ως: {filename}")

except Exception as e:
    print(f"Σφάλμα: {e}")

finally:
    driver.quit()
