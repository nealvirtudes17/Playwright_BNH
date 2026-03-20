from playwright.sync_api import sync_playwright, Playwright
from rich import print
import json


def run(playwright: Playwright):
    #start_url = "https://www.bing.com/turing/captcha/challenge"
    start_url = "https://www.bhphotovideo.com/c/product/1663582-REG/canon_rf_16mm_f_2_8_stm.html"
    chrome = playwright.chromium
    browser = chrome.launch(headless=False)
    page = browser.new_page()
    page.goto(start_url)

    page.wait_for_timeout(10000)

    page.close()


with sync_playwright() as playwright:
    run(playwright)