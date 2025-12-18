import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import json
import os
import pandas as pd

COOKIES_FILE = "cookies.json"


# ---------------------------------------------------
# HUMANIZED MESSAGES
# ---------------------------------------------------
CONNECTION_NOTE = (
    "Hi {name}, I came across your profile and felt it would be nice to connect. "
    "I spend time thinking about reflection and how people handle the mental load of work and life. "
)

FOLLOWUP_MSG = (
    "Hey, thanks for accepting. "
    "I have been building something personal called Sentari AI. "
    "It is a simple journaling tool that helps you see patterns you keep repeating without realizing it. "
    "You talk for a few minutes and a week later you see what keeps coming up. "
    "If you want to try it sometime I would love to show you."
)


# ---------------------------------------------------
# DRIVER
# ---------------------------------------------------
def start_driver():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)
    return driver


# ---------------------------------------------------
# COOKIE SAVE / LOAD
# ---------------------------------------------------
def save_cookies(driver):
    with open(COOKIES_FILE, "w") as f:
        json.dump(driver.get_cookies(), f)


def load_cookies(driver):
    if not os.path.exists(COOKIES_FILE):
        return False

    driver.get("https://www.linkedin.com")
    time.sleep(2)

    with open(COOKIES_FILE, "r") as f:
        cookies = json.load(f)

    for c in cookies:
        try:
            driver.add_cookie(c)
        except:
            pass

    driver.refresh()
    time.sleep(3)
    return True


# ---------------------------------------------------
# CHECK LOGIN STATE
# ---------------------------------------------------
def is_logged_in(driver):
    try:
        driver.find_element(By.ID, "global-nav")
        return True
    except:
        return False


# ---------------------------------------------------
# DEBUG: PRINT ALL BUTTONS
# ---------------------------------------------------
def debug_buttons(driver, url):
    driver.get(url)
    time.sleep(3)

    print("\n=================== DEBUG BUTTONS ===================")
    btns = driver.find_elements(By.TAG_NAME, "button")
    for b in btns:
        try:
            print("BUTTON:", b.text)
        except:
            pass
    print("================= END DEBUG BUTTONS =================\n")


# ---------------------------------------------------
# DEBUG: PRINT MORE MENU ITEMS
# ---------------------------------------------------
def debug_more_menu(driver, url):
    driver.get(url)
    time.sleep(3)

    print("\n===== DEBUG MORE MENU =====")
    try:
        # Use the REAL header More actions button
        more_btn = driver.find_element(
            By.XPATH, "//button[@aria-label='More actions' and contains(@id,'profile-overflow')]"
        )
        driver.execute_script("arguments[0].click();", more_btn)
        time.sleep(1)

        items = driver.find_elements(By.XPATH, "//div[@role='menu']//span")
        for it in items:
            print("MENU ITEM:", it.text)

    except Exception as e:
        print("Could not open More menu:", e)

    print("===== END MORE MENU DEBUG =====\n")

def find_and_click_connect(driver):
    selectors = [
        "//button[normalize-space()='Connect']",
        "//button//span[normalize-space()='Connect']/ancestor::button",
        "//span[normalize-space()='Connect']/ancestor::div[@role='button']",
        "//button[@data-control-name='connect']",
        "//button[contains(@aria-label, 'Connect')]",
        "//*[normalize-space()='Connect' and (self::button or self::div or self::span)]",
        "//a[normalize-space()='Connect']",
    ]

    for xp in selectors:
        try:
            el = driver.find_element(By.XPATH, xp)
            driver.execute_script("arguments[0].scrollIntoView(true);", el)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", el)
            print(f"Clicked Connect using selector: {xp}")
            return True
        except:
            continue

    print("Could not find ANY Connect button variant.")
    return False

# ---------------------------------------------------
# SEND CONNECTION REQUEST (FINAL VERSION)
# ---------------------------------------------------
def find_and_click_connect(driver):
    selectors = [
        "//button[normalize-space()='Connect']",
        "//button//span[normalize-space()='Connect']/ancestor::button",
        "//span[normalize-space()='Connect']/ancestor::div[@role='button']",
        "//button[@data-control-name='connect']",
        "//button[contains(@aria-label, 'Connect')]",
        "//*[normalize-space()='Connect' and (self::button or self::div or self::span)]",
        "//a[normalize-space()='Connect']",
    ]

    for xp in selectors:
        try:
            el = driver.find_element(By.XPATH, xp)
            driver.execute_script("arguments[0].scrollIntoView(true);", el)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", el)
            print(f"Clicked Connect using selector: {xp}")
            return True
        except:
            continue

    print("Could not find ANY Connect button variant.")
    return False



def send_connection_request(driver, name, url):
    print("\n--- DEBUGGING THIS PROFILE:", name, "---")

    debug_buttons(driver, url)
    debug_more_menu(driver, url)

    driver.get(url)
    time.sleep(4)

    # Always scroll to top
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

    clicked = False

    # Try universal Connect button first
    if find_and_click_connect(driver):
        clicked = True
        time.sleep(2)
    else:
        print("Universal Connect not found. Trying More actions…")

    # Try More → Connect fallback
    if not clicked:
        try:
            more_btn = driver.find_element(
                By.XPATH,
                "//button[@aria-label='More actions' and contains(@id,'profile-overflow')]"
            )
            driver.execute_script("arguments[0].click();", more_btn)
            print("Opened More actions dropdown")
            time.sleep(1)

            connect_inside = driver.find_element(
                By.XPATH, "//div[@role='menuitem']//span[normalize-space()='Connect']"
            )
            driver.execute_script("arguments[0].click();", connect_inside)
            print("Clicked Connect inside More actions")
            time.sleep(2)
            clicked = True

        except Exception as e:
            print("Could NOT find Connect inside More actions!")
            print("ERROR:", e)
            return False

    # Popup: Add a note
    try:
        add_note_btn = driver.find_element(
            By.XPATH, "//button[normalize-space()='Add a note']"
        )
        add_note_btn.click()
        time.sleep(1)

        msg = CONNECTION_NOTE.format(name=name)[:290]
        textarea = driver.find_element(By.XPATH, "//textarea")
        textarea.send_keys(msg)
        time.sleep(1)

        send_btn = driver.find_element(
            By.XPATH, "//button[normalize-space()='Send']"
        )
        send_btn.click()
        print("Connection with note sent to", name)
        return True

    except:
        print("No Add a note button → trying Send without note…")

    # Popup: Send without a note
    try:
        send_wo = driver.find_element(
            By.XPATH, "//button[normalize-space()='Send without a note']"
        )
        send_wo.click()
        print("Connection (no note) sent to", name)
        return True

    except:
        print("FAILED: No send buttons found. Popup did not appear.")
        return False


# ---------------------------------------------------
# CHECK IF ACCEPTED
# ---------------------------------------------------
def check_accepted(driver, url):
    try:
        driver.get(url)
        time.sleep(3)
        driver.find_element(By.XPATH, "//button[contains(., 'Message')]")
        return True
    except:
        return False


# ---------------------------------------------------
# SEND FOLLOW UP
# ---------------------------------------------------
def send_followup(driver, name, url):
    try:
        driver.get(url)
        time.sleep(3)

        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        # Try the REAL header message button (best selector)
        try:
            msg_btn = driver.find_element(
                By.XPATH,
                "//button[@data-control-name='message']"
            )
            driver.execute_script("arguments[0].click();", msg_btn)
            print("Opened header message box")
        except:
            # fallback selector for some UIs
            try:
                msg_btn = driver.find_element(
                    By.XPATH,
                    "//button[contains(@aria-label,'Message') and contains(@id,'ember')]"
                )
                driver.execute_script("arguments[0].click();", msg_btn)
                print("Opened header message box (fallback)")
            except Exception as e:
                print("FAILED: Could not find the real header Message button")
                print("Error:", e)
                return False

        time.sleep(2)

        # message textbox is always inside this class
        box = driver.find_element(
            By.XPATH, "//div[contains(@class,'msg-form__contenteditable')]"
        )
        box.click()
        time.sleep(0.5)
        box.send_keys(FOLLOWUP_MSG)
        time.sleep(1)

        send_btn = driver.find_element(
            By.XPATH, "//button[contains(@class,'msg-form__send-button')]"
        )
        send_btn.click()

        print("Follow up sent to", name)
        return True

    except Exception as e:
        print("Follow up FAILED for", name)
        print("Error:", e)
        return False


# ---------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------
if __name__ == "__main__":
    df = pd.read_csv("people.csv")
    driver = start_driver()

    cookies_loaded = load_cookies(driver)

    if not cookies_loaded or not is_logged_in(driver):
        print("Please login manually, then press ENTER here.")
        driver.get("https://www.linkedin.com/login")
        input()
        save_cookies(driver)
        print("Session saved. Future logins will be automatic.")

    while True:
        for i, row in df.iterrows():
            name = row["name"]
            url = row["profile_url"]
            status = row.get("status", "")

            if status == "":
                success = send_connection_request(driver, name, url)
                if success:
                    df.loc[i, "status"] = "connection_sent"
                    df.to_csv("people.csv", index=False)

            elif status == "connection_sent":
                if check_accepted(driver, url):
                    if send_followup(driver, name, url):
                        df.loc[i, "status"] = "followup_sent"
                        df.to_csv("people.csv", index=False)

        print("Waiting 20 minutes before next check...")
        time.sleep(1200)
