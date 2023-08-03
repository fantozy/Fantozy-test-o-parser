import re
from typing import List, Union

from bs4 import BeautifulSoup


def extract_numeric_value(raw_string):
    numeric_string = re.sub(r"[^\d.]", "", raw_string)

    try:
        if "." in numeric_string:
            return float(numeric_string)
        else:
            return int(numeric_string)
    except ValueError:
        # Handle conversion errors
        print("Error: Unable to convert value to numeric.")
        return None


def lookup_prices(product: BeautifulSoup) -> List[Union[str, int]]:
    price_div = (
        product.find("div", recursive=False)
        .find("div", recursive=False)
        .find("div", recursive=False)
        .find_all("span")
    )
    [price, old_price, discount] = [
        price_div[0].text.strip(),
        price_div[1].text.strip(),
        price_div[2].text.strip(),
    ]
    price = extract_numeric_value(price)
    old_price = extract_numeric_value(old_price)

    return [price, old_price, discount]


def extract_name(product: BeautifulSoup) -> str:
    name_div = product.find("div", recursive=False)
    return (
        name_div.find("a")
        .find("div")
        .find("span")
        .text.strip()
        .replace("\n", "")
        .replace("\t", "")
    )


def extract_rating_and_comments(product: BeautifulSoup) -> List[Union[str, int]]:
    rating_div = product.find("div", recursive=False)
    rating_comment = (
        rating_div.find("a")
        .find_next_sibling("div")
        .find("div")
        .find_all("span", recursive=False)
    )
    rating = rating_comment[0].text.strip()
    feedback = rating_comment[1].text.strip()

    return [rating, feedback]
