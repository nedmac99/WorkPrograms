"""
Import libraries used for data scraper
Requests to get information from webpage
BeautifulSoup to parse(analyze) the information and content
"""

import requests
from bs4 import BeautifulSoup

# Define Target URL
url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, "html.parser")

products = soup.select("div.thumbnail")

product_list = []

for product in products:
    title = product.select_one("a.title").text.strip()
    price_text = product.select_one("h4.price").text.strip().replace("$", "")
    description = product.select_one("p.description").text.strip()

    try:
        price = float(price_text)
    except ValueError:
        continue

    product_list.append({"title": title, "price": price, "description": description})


def get_price(product):
    return product["price"]


sorted_products = sorted(product_list, key=get_price, reverse=True)

print("Top 10 Most Expensive Laptops: \n")

for i, product in enumerate(sorted_products[:10], start=1):
    print(f"{i}. {product['title']} - ${product['price']:.2f}")
    print(f"   {product['description']}\n")
