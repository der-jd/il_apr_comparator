import time
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


URL_CAKEDEFI_LM = "https://app.cakedefi.com/liquidity-mining"
REGEX_HTML_COIN_PAIR_BLOCK = ".*coinTextMedium.*"
REGEX_HTML_APR_BLOCK = ".*tableCellLeft.*tableCell.*"


def get_apr_from_cakedefi(coin_pair: tuple[str, str]) -> float:
    print(f"Search for APR of coin pair '{coin_pair[0]}-{coin_pair[1]}'")
    print(f"Get HTML content of {URL_CAKEDEFI_LM}...")

    browser = webdriver.Chrome()
    browser.get(URL_CAKEDEFI_LM)
    try:
        seconds_to_wait_for_javascript_content = 5
        print(f"Wait {seconds_to_wait_for_javascript_content} seconds until Javascript content is loaded...")
        WebDriverWait(browser, seconds_to_wait_for_javascript_content).until(time.sleep(seconds_to_wait_for_javascript_content + 3))
    except Exception: # pylint: disable=broad-exception-caught
        print("Timeout/exception on purpose: wait time is over!")
    html = browser.page_source

    soup = BeautifulSoup(html, "lxml")
    coin_pair_blocks = soup.find_all('span', {'class': re.compile(REGEX_HTML_COIN_PAIR_BLOCK)})
    print(f"Found coin pairs:\n{[p.get_text().strip() for p in coin_pair_blocks]}")

    if not coin_pair_blocks:
        raise RuntimeError("ERROR: HTML tags which contain coin pairs not found!")

    for b in coin_pair_blocks:
        # Alternative if-pattern/-approach. Just for documentation.
        # if b.find('span', {'class': re.compile(".*coinText.*")}, string = "BCH") and b.find('span', {'class': re.compile(".*coinText.*")}, string = "-DFI"):
        if re.match(f"{coin_pair[0]}\n?-\n?{coin_pair[1]}", b.get_text().strip(), re.IGNORECASE) or \
           re.match(f"{coin_pair[1]}\n?-\n?{coin_pair[0]}", b.get_text().strip(), re.IGNORECASE): # e.g. "BCH-DFI" or "DFI-BCH"
            print(f"Requested coin pair '{coin_pair[0]}-{coin_pair[1]}' found!")
            print("Search for corresponding APR...")
            apr_block = b.find_next('div', {'class': re.compile(REGEX_HTML_APR_BLOCK)})

            if re.match(r"\bAPR[0-9]?", apr_block.get_text().strip()): # \b: match beginning of a word
                return float(re.search(r"[0-9]+\.[0-9]+", apr_block.get_text().strip()).group(0))

            raise RuntimeError(f"ERROR: APR of coin pair '{coin_pair[0]}-{coin_pair[1]}' not found!")

    raise RuntimeError(f"ERROR: Coin pair '{coin_pair[0]}-{coin_pair[1]}' not found!")
