from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Selenium WebDriver
options = Options()
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Open the webpage
url = "https://www.gvpta.ca/vancouver-theatre-guide"
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Locate iframe and switch to it
try:
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    driver.switch_to.frame(iframe)
    print("Switched to iframe.")
except Exception as e:
    print(f"Error switching to iframe: {e}")
    driver.quit()
    exit()

# Extract content within the iframe
try:
    # Example: Extract all text or specific elements
    elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'SimpleListEvent')]")
    print(f"Found {len(elements)} elements with class 'SimpleListEvent'.")

    # Extract recursive data from elements
    def extract_recursive(element):
        data = {"anchors": [], "spans": [], "tds": []}

        try:
            anchors = element.find_elements(By.TAG_NAME, "a")
            for anchor in anchors:
                data["anchors"].append(anchor.text.strip())
        except Exception as e:
            print(f"Error extracting anchors: {e}")

        try:
            spans = element.find_elements(By.TAG_NAME, "span")
            for span in spans:
                data["spans"].append(span.text.strip())
        except Exception as e:
            print(f"Error extracting spans: {e}")

        try:
            tds = element.find_elements(By.TAG_NAME, "td")
            for td in tds:
                data["tds"].append(td.text.strip())
        except Exception as e:
            print(f"Error extracting tds: {e}")

        return data

    # Process and display data
    event_list = []
    for element in elements:
        event_list.append(extract_recursive(element))

    for idx, event in enumerate(event_list, start=1):
        print(f"\nEvent {idx}:")
        print(f"Anchors: {', '.join(event['anchors'])}")
        print(f"Spans: {', '.join(event['spans'])}")
        print(f"Tds: {', '.join(event['tds'])}")
except Exception as e:
    print(f"Error extracting data: {e}")

# Quit driver
driver.quit()
