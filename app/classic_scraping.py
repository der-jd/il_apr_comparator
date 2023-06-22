"""
Scrape website with BeautifulSoup and Selenium.

ATTENTION:
This code does not work inside an AWS Lambda function because Chrome keeps crashing!
However it works locally, outside and inside of a container.
"""

import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions


URL_BAKE_LM = "https://app.bake.io/liquidity-mining"
REGEX_HTML_COIN_PAIRS_BLOCK = ".*cryptoPairTable.*"
REGEX_HTML_COIN_PAIR_BLOCK = ".*coinTextMedium.*"
REGEX_HTML_APR_BLOCK = ".*tableCellLeft.*tableCell.*"


def get_apr() -> list[dict]:
    print("Scrape the Bake website to get the APR values...")
    print(f"Get HTML content of {URL_BAKE_LM}...")

    chrome_options = ChromeOptions()
    # Attention: Running Chrome without sandboxing is not best-practice!
    # Unfortunately I didn't find any solution to run Chrome with sandboxing in a Docker container.
    chrome_options.add_argument('--no-sandbox')
    chrome_options.headless = True
    driver = webdriver.Chrome(options = chrome_options)

    driver.get(URL_BAKE_LM)
    try:
        seconds_to_wait_for_javascript_content = 5
        print(f"Wait {seconds_to_wait_for_javascript_content} seconds until Javascript content is loaded...")
        WebDriverWait(driver, seconds_to_wait_for_javascript_content).until(time.sleep(seconds_to_wait_for_javascript_content + 3))
    except Exception: # pylint: disable = broad-exception-caught
        print("Timeout/exception on purpose: wait time is over!")
    html = driver.page_source

    soup = BeautifulSoup(html, "lxml")
    block_with_cryptocurrencies = soup.find('div', {'class': re.compile(REGEX_HTML_COIN_PAIRS_BLOCK)})
    # Ignore two pyright errors in the following line (don't know how to fix them).
    coin_pair_blocks = block_with_cryptocurrencies.find_all('span', {'class': re.compile(REGEX_HTML_COIN_PAIR_BLOCK)}) # pyright: ignore [reportGeneralTypeIssues, reportOptionalMemberAccess]
    print(f"Found coin pairs:\n{[p.get_text().strip() for p in coin_pair_blocks]}")

    if not coin_pair_blocks:
        raise RuntimeError("ERROR: HTML tags which contain coin pairs not found!")

    result = []
    for b in coin_pair_blocks:
        symbols = b.get_text().strip()
        print(f"Found '{symbols}'")

        print("Search for corresponding APR...")
        apr_block = b.find_next('div', {'class': re.compile(REGEX_HTML_APR_BLOCK)})

        if re.match("APR[0-9]?", apr_block.get_text().strip()): # 'match' checks for a match only at the beginning of the string
            match_obj = re.search(r"[0-9]+\.?[0-9]*", apr_block.get_text().strip())
            if match_obj:
                apr = float(match_obj.group(0))
                print(f"Found: {symbols} --> {apr} %")
                print("----------------------------")
                result.append({
                    "symbols": symbols,
                    "coin_1": {
                        "id": "",
                        "symbol": symbols.split('-')[0],
                        "name": ""
                    },
                    "coin_2": {
                        "id": "",
                        "symbol": symbols.split('-')[1],
                        "name": ""
                    },
                    "apr": apr
                })
            else:
                raise RuntimeError(f"ERROR: Value for APR of coin pair '{symbols}' not found!")
        else:
            raise RuntimeError(f"ERROR: APR block of coin pair '{symbols}' not found!")

    return result
