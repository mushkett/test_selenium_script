import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def test_shopping(driver):
    product = 'macbook air m1 16gb'
    browser = driver
    amazon_price = 0
    bestbuy_price = 0

    try:

        # AMAZON
        browser.get("https://www.amazon.com/")
        search = browser.find_element(By.ID, "twotabsearchtextbox")
        search.clear()
        search.send_keys(product)

        search.send_keys(Keys.ENTER)

        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.find_all('div', {"class": "s-result-item"})

        browser.find_element(By.CSS_SELECTOR, "a.s-pagination-next").click()
        html_page_2 = browser.page_source
        soup = BeautifulSoup(html_page_2, 'html.parser')
        cards_page_2 = soup.find_all('div', {"class": "s-result-item"})

        cards.extend(cards_page_2)

        list_of_cards_values = []

        for card in cards:
            card_values = {}

            price = card.find('span', {'class': 'a-price-whole'})

            if price:
                try:
                    price = price.get_text()

                    numeric_filter = filter(str.isdigit, price)
                    numeric_string = ''.join(numeric_filter)

                    price = int(numeric_string)

                    card_values['price'] = price

                    reviews_counter = card.find('span',
                                                {'class': 's-underline-text'})

                    if reviews_counter:

                        reviews_counter = reviews_counter.get_text()

                        numeric_filter = filter(str.isdigit, reviews_counter)
                        numeric_string = ''.join(numeric_filter)

                        reviews_counter = int(numeric_string)

                        if reviews_counter >= 500:
                            list_of_cards_values.append(card_values)
                        else:
                            continue
                    else:
                        continue
                except Exception as ex:
                    print(ex)
                    print('Amazon')

            else:
                continue

        amazon_price = min([item["price"] for item in list_of_cards_values])

        # BESTBUY

        browser.get("https://www.bestbuy.com/")
        time.sleep(2)
        search = browser.find_element(By.ID, "gh-search-input")
        search.clear()
        search.send_keys(product)

        search.send_keys(Keys.ENTER)
        time.sleep(5)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.find_all('li', {"class": "sku-item"})

        list_of_cards_values = []

        for card in cards:
            card_values = {}

            price = card.find('div', {'class': 'priceView-hero-price'})\
                .find('span')

            if price:
                price = price.get_text()

                try:

                    numeric_filter = filter(str.isdigit, price)
                    numeric_string = ''.join(numeric_filter)

                    price = int(numeric_string[:-2])

                    card_values['price'] = price

                    reviews_counter = card.find('span', {'class': 'c-reviews'})

                    if reviews_counter:

                        reviews_counter = reviews_counter.get_text()

                        numeric_filter = filter(str.isdigit, reviews_counter)
                        numeric_string = ''.join(numeric_filter)

                        reviews_counter = int(numeric_string)

                        if reviews_counter >= 500:

                            list_of_cards_values.append(card_values)
                        else:
                            continue
                    else:
                        continue
                except Exception as ex:
                    print(ex)
            else:
                continue

        bestbuy_price = min([item["price"] for item in list_of_cards_values])

    except Exception as ex:
        print(ex)
        print('BBuy')
    finally:
        browser.close()
        browser.quit()

    # once script completed the line below should be uncommented.
    assert amazon_price > bestbuy_price
