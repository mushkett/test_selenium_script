from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def test_shopping(driver):
    product = 'macbook air m1 16gb'
    browser = webdriver.Chrome(r"D:\PythonProjects\Test_task\chromedriver\chromedriver.exe")

    try:
        browser.get("https://www.amazon.com/")
        search = browser.find_element(By.ID, "twotabsearchtextbox")
        search.clear()
        search.send_keys(product)

        search.send_keys(Keys.ENTER)

        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.find_all('div', {"class": "s-result-item"})
        list_of_cards_values = []

        for card in cards:
            card_values = {}

            price = card.find('span', {'class': 'a-price-whole'})

            if price:
                price = price.get_text()
                if ',' in price or '.' in price:
                    price = int(price.replace(',', '').replace('.', ''))
                    card_values['price'] = price
                else:
                    card_values['price'] = int(price)

                reviews_counter = card.find('span', {'class': 's-underline-text'})

                if reviews_counter:

                    reviews_counter = reviews_counter.get_text()

                    if ',' in reviews_counter:

                        reviews_counter = int(reviews_counter.replace(',', ''))
                    else:

                        reviews_counter = int(reviews_counter)

                    card_values['reviews'] = reviews_counter
                    card_values['card'] = card

                    list_of_cards_values.append(card_values)
                else:
                    continue
            else:
                continue

        for i in list_of_cards_values:
            print(f"Price: {i['price']}")
            print(f"Reviews: {i['reviews']}")
            print('')

    except Exception as ex:
        print(ex)
    finally:
        browser.close()
        browser.quit()

    # once script completed the line below should be uncommented.
    # assert amazon_price > bestbuy_price
