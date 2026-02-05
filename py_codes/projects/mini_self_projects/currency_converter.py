import requests
from bs4 import BeautifulSoup
import re

url = "https://www.x-rates.com/table/?from=USD&amount=1"
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, "html.parser")

pattern = r'(to=\w+)">([\d.]+)</a>'

rates = soup.select("td.rtRates")

currency_symbols = ["£", "€", "¥", "$", "₿"]


def main():

    currency_choice = input(
        "Enter currency to convert to: \n1. Pounds\n2. Euro\n3. Japanese Yen\n4. Austrailian Dollar\n5. Canadian Dollars\n"
    )
    for rate in rates:
        to_currency = str(rate.select_one("a"))
        conversion_link = re.search(pattern, to_currency)

        if conversion_link:
            conversion_type = conversion_link.group(1)
            global conversion
            conversion = conversion_link.group(2)

        if currency_choice == "1":
            if conversion_type == "to=GBP":
                print(
                    convert_to_pounds(
                        input(
                            "Enter currency in USD to see coversion to British Pounds: $"
                        )
                    )
                )
                break
        elif currency_choice == "2":
            if conversion_type == "to=EUR":
                print(
                    convert_to_euro(
                        input("Enter currency in USD to see coversion to Euros: $")
                    )
                )
                break
        elif currency_choice == "3":
            if conversion_type == "to=JPY":
                print(
                    convert_to_jyen(
                        input(
                            "Enter currency in USD to see coversion to Japanese Yen: $"
                        )
                    )
                )
                break
        elif currency_choice == "4":
            if conversion_type == "to=AUD":
                print(
                    convert_to_ausd(
                        input(
                            "Enter currency in USD to see coversion to Austrailian dollars: $"
                        )
                    )
                )
                break
        elif currency_choice == "5":
            if conversion_type == "to=CAD":
                print(
                    convert_to_ausd(
                        input(
                            "Enter currency in USD to see coversion to Canadian dollars: $"
                        )
                    )
                )
                break

        else:
            print("Invalid Choice")
            break


# Conversions
def convert_to_pounds(n):
    n = float(n) * float(conversion)
    return f"{currency_symbols[0]}{n}"


def convert_to_euro(n):
    n = float(n) * float(conversion)
    return f"{currency_symbols[1]}{n}"


def convert_to_jyen(n):
    n = float(n) * float(conversion)
    return f"{currency_symbols[2]}{n}"


def convert_to_ausd(n):
    n = float(n) * float(conversion)
    return f"{currency_symbols[3]}{n}"


def convert_to_cand(n):
    n = float(n) * float(conversion)
    return f"{currency_symbols[4]}{n}"


if __name__ == "__main__":
    main()
