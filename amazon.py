from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import textwrap
import csv
import re


def get_amazon_page_info(url):
    text = ""
    # ヘッドレスでの実行が必要になるため、ヘッドレスで必要なオプションを追加します。
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(20)

    browser.get(url)
    text = browser.page_source
    browser.quit()

    return text

def get_amazon_price(url):
    text = get_amazon_page_info(url)
    amazon_bs = BeautifulSoup(text, features="lxml")
    aod = amazon_bs.find_all(id="aod-offer")
    amazon_bs = BeautifulSoup(text, features="lxml")
    aod_sb_pinned = amazon_bs.find_all(id="aod-pinned-offer")
    amazon_bs = BeautifulSoup(text, features="lxml")
    aod_sb = amazon_bs.find_all(id="aod-offer-soldBy")
    soldby = []
    #print(aod_sb)
    for sb in aod_sb:
        if re.search("Amazon.co.jp", str(sb)) is not None:
            soldby.append(re.search("Amazon.co.jp", str(sb)).group())
        else:
            soldby.append("marketplace")


    prices = []
    if not len(aod_sb_pinned) == 0:
        soldby = soldby[1:]
        for offer in aod_sb_pinned:
            prices.append(offer.select('.a-price-whole')[0])
    print(soldby)

    for offer in aod:
        prices.append(offer.select('.a-price-whole')[0])
    prices = [int(str(price).replace('<span class="a-price-whole">', '').replace('</span>', '').replace(',', '')) for price in prices]
    print(prices)