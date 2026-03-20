import locale

from playwright.sync_api import sync_playwright, Playwright
from rich import print
import json
from seleniumbase import sb_cdp


sb = sb_cdp.Chrome(locale="en")
end_point_url = sb.get_endpoint_url()


def run(playwright: Playwright):
    start_url = "https://www.bhphotovideo.com/deals-promotions-coupons/Lenses/ci/15492/N/4288584250/pn/24"
    browser = playwright.chromium.connect_over_cdp(end_point_url)
    context = browser.contexts[0]

    page = context.pages[0]
    #page.route("**/*.{png,jpg,jpeg}", lambda route: route.abort)
    page.goto(start_url, wait_until="domcontentloaded", timeout=60000)

    sb.sleep(5)

    while True:
        for link in page.locator(
            "a[data-selenium='miniProductPageDetailsGridViewNameLink']"
        ).all()[:1]:
            p = browser.new_page(base_url="https://www.bhphotovideo.com")
            #p.route("**/*.{png,jpg,jpeg}", lambda route: route.abort)

            url = link.get_attribute("href")

            if url is not None:
                p.goto(url)

                sb.sleep(5)

                sb.solve_captcha()

                sb.sleep(5)
            else:
                p.close()
            
            data = p.locator("script[type='application/ld+json']").nth(1).text_content()

            json_data = json.loads(data)

            print(json_data['name'])

            p.close()
        
        next_button = page.locator("a[data-selenium='listingPagingPageNext']")

        is_disabled = next_button.locator("svg[class*='Disabled']").count() > 0

        if is_disabled:
            print("Reached the end of the line. Breaking.")
            break
        else:
            print("Next page is available. Clicking...")

            current_url = page.url

            next_button.click()

            print("Waiting for new page to load...")
            page.wait_for_function(f"window.location.href !== '{current_url}'")

            sb.sleep(4)
    
    browser.close()
            

with sync_playwright() as playwright:
    run(playwright)