# import time
# import asyncio
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as ec
# from selenium.webdriver.support.ui import WebDriverWait
#
# from webdriver_manager.chrome import ChromeDriverManager
# from scraper import scraper
#
#
# def main():
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     url = 'https://twitter.com/CampusFrance_DZ'
#     driver.get(url)
#     time.sleep(5)
#     resp = driver.page_source
#     # driver.close()
#     scraper(resp)
#
#
# main()

from playwright.sync_api import sync_playwright
from webdriver_manager.chrome import ChromeDriverManager


def scrape_tweet(url: str) -> dict:
    """
    Scrape a single tweet page for Tweet thread e.g.:
    https://twitter.com/Scrapfly_dev/status/1667013143904567296
    Return parent tweet, reply tweets and recommended tweets
    """
    _xhr_calls = []

    def intercept_response(response):
        """capture all background requests and save them"""
        # we can extract details from background requests
        if response.request.resource_type == "xhr":
            _xhr_calls.append(response)
        return response

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        # enable background request intercepting:
        page.on("response", intercept_response)
        # go to url and wait for the page to load
        page.goto(url)
        page.wait_for_selector("[data-testid='tweet']")

        # find all tweet background requests:
        tweet_calls = [f for f in _xhr_calls if "TweetResultByRestId" in f.url]
        for xhr in tweet_calls:
            data = xhr.json()
            return data['data']['tweetResult']['result']


if __name__ == "__main__":
    print(scrape_tweet("https://twitter.com/Scrapfly_dev/status/1664267318053179398"))
