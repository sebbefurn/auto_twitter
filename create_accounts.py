from playwright.sync_api import sync_playwright, Page
import time
from discord_bot import random_sleep
from fetch_gmail import get_codes
import credentials

def main():
    try:
        browser = None
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto("https://twitter.com/i/flow/signup")
            random_sleep()
            page.get_by_text("Create account").click()
            random_sleep()
            page.get_by_label("Name").fill("John")
            random_sleep()
            page.get_by_label("Email").fill("John.lol@gmail.com")
            random_sleep()
            page.locator("#SELECTOR_1").select_option('August')
            random_sleep()
            page.locator("#SELECTOR_2").select_option('5')
            random_sleep()
            page.locator("#SELECTOR_3").select_option('2003')
            random_sleep()
            page.get_by_role("button", name="Next").click()
            random_sleep()
            page.get_by_role("button", name="Next").click()
            random_sleep()
            page.get_by_role("button", name="Sign up").click()
            time.sleep(5)

            # Now you need to grab the verification code from gmail and put it into the field

            codes = get_codes("furngaming1@gmail.com", credentials.app_password)

            page.get_by_label("Password").fill(credentials.password)
            random_sleep()
            # Can upload image if you want
            page.get_by_role("button", name="Skip for now").click()
            time.sleep(5)
    except:
        print("Couldn't start")
            
main()