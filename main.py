import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


# If reCAPTCHA is encountered, consider using a service like 2Captcha
# from twocaptcha import TwoCaptcha

def search_realtor():
    # Get values from the form
    city = city_entry.get()

    # --- Selenium ---
    # Set up the WebDriver
    driver = webdriver.Chrome()
    driver.get("https://www.realtor.ca/")

    # --- Handle potential early reCAPTCHA ---
    try:
        recaptcha_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))
        )
        print("Please solve the reCAPTCHA.")
        WebDriverWait(driver, 3600).until(
            EC.invisibility_of_element_located((By.ID, "recaptcha-anchor"))
        )
        print("reCAPTCHA solved!")
    except:
        print("No reCAPTCHA found on the initial page.")

    # --- Handle cookies ---
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "TOUMsgCon"))
    )
    dismiss_button = driver.find_element(By.ID, "TOUdismissBtn")
    dismiss_button.click()

    # --- Search ---
    search_bar = driver.find_element(By.ID, "homeSearchTxt")
    search_bar.send_keys(city)
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "homeSearchBtn"))
    )
    search_button.click()

    # --- Handle reCAPTCHA (if it appears again after the search) ---
    try:
        recaptcha_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))
        )
        print("Please solve the reCAPTCHA.")
        WebDriverWait(driver, 3600).until(
            EC.invisibility_of_element_located((By.ID, "recaptcha-anchor"))
        )
        print("reCAPTCHA solved!")
    except:
        print("No reCAPTCHA found after search.")

    # --- Wait for map page to load ---
    WebDriverWait(driver, 10).until(
        EC.url_contains("https://www.realtor.ca/map")
    )

    # --- Click the Search button on the map page ---
    try:
        search_button_map = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btnMapSearch"))
        )
        print("Map search button found!")

        # Using JavaScript to click the button directly
        driver.execute_script("arguments[0].click();", search_button_map)
        print("Map search initiated.")
    except TimeoutException:
        print("Timeout: Could not find the map search button within the time limit.")
    except NoSuchElementException:
        print("NoSuchElement: Map search button could not be found on the page.")
    except Exception as e:
        print("Error clicking map search button:", e)

    # Keep the browser open after execution
    print("Search completed, keeping the browser open...")
    time.sleep(600)


# --- Tkinter ---
root = tk.Tk()
root.title("Realtor.ca Search")

# --- Form elements ---
city_label = ttk.Label(root, text="City:")
city_label.grid(row=0, column=0)
city_entry = ttk.Entry(root)
city_entry.grid(row=0, column=1)

search_button = ttk.Button(root, text="Search", command=search_realtor)
search_button.grid(row=5, column=1)

root.mainloop()
