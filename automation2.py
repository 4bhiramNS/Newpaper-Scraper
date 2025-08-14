from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime



# Setup
website = "https://www.bbc.com/news"
path = r"C:\Users\abhir\OneDrive\Documents\chromedriver-win64\chromedriver.exe"
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)
driver.get(website)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)  # Wait for content to load

# Now re-fetch news_cards after scroll
news_cards = driver.find_elements(By.XPATH, "//div[@data-testid='card-text-wrapper']")
# Wait for headlines to load (max 10 seconds)
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h2[@data-testid='card-headline']"))
    )
except:
    print("Timeout: Headlines did not load.")
    driver.quit()
    exit()

# Now get news cards
news_cards = driver.find_elements(By.XPATH, "//div[@data-testid='card-text-wrapper']")

head = []
desc = []

for card in news_cards:
    try:
        headline_elem = card.find_element(By.XPATH, ".//h2[@data-testid='card-headline']")
        description_elem = card.find_element(By.XPATH, ".//p[@data-testid='card-description']")

        headline_text = headline_elem.text.strip()
        description_text = description_elem.text.strip()

        if headline_text and description_text:
            head.append(headline_text)
            desc.append(description_text)

    except Exception:
        continue

driver.quit()

# Save if data found
if head and desc:
    df_news = pd.DataFrame({"head": head, "desc": desc})
    date_str = datetime.now().strftime("%Y-%m-%d")
    df_news.to_csv(f"news_{date_str}.csv", index=False)
    print(f"Saved {len(head)} news items.")
else:
    print("No news items found. CSV not created.")
