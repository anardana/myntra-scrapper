import logging
import os
import pathlib
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException

url = "https://www.myntra.com/men-formal-shirts?f=Print_or_Pattern_Type_article_attr%3Asolid%3A%3ASleeve_Length_article_attr%3Along%20sleeves%3A%3Abrand%3ABritish%20Club"
download_dir = "/Users/1021839/data/shirt/long_sleeve_solid"

pathlib.Path(download_dir).mkdir(parents=True, exist_ok=True)

logging.getLogger().setLevel(logging.INFO)

WAIT_TIME = 1
driver = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'))
driver.implicitly_wait(WAIT_TIME)

logging.info("Opening URL: %s", url)
driver.get(url)

counter = 1
time.sleep(WAIT_TIME)
while True:
    counter = counter + 1
    try:
        show_more_products_link = driver.find_element_by_class_name("results-showmore")
        time.sleep(WAIT_TIME)
        logging.info("  Clicking Show More(%d)", counter)
        show_more_products_link.click()
    except NoSuchElementException:
        logging.info("No More products to show on page")
        break
    except WebDriverException:
        logging.warning("Show more is not clickable")
        time.sleep(WAIT_TIME)

time.sleep(10)
product_divs = driver.find_elements_by_xpath("//*[@id=\"desktopSearchResults\"]/div[2]/section/ul/li")

product_urls = []

for product_div in product_divs:
    link = product_div.find_element_by_xpath("a")
    product_urls.append(link.get_attribute("href"))

number_of_products = len(product_urls)
logging.info("Scrapped product URLs. Going to scrape %d images", number_of_products)

counter = 1
for product_url in product_urls:
    logging.info("Scraping image (%d:%d)", counter, number_of_products)
    driver.get(product_url)
    counter = counter + 1
    while True:
        try:
            image = driver.find_element_by_class_name("thumbnails-selected-image").get_attribute("src")
            r = requests.get(image)
            with open(os.path.join(download_dir, image.split("/")[-1]), 'wb') as f:
                f.write(r.content)
            break
        except NoSuchElementException:
            logging.info("Unable to download image. Retrying: %s", url)
            time.sleep(WAIT_TIME)

driver.close()
