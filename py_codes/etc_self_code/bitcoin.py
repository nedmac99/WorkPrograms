# In a file called bitcoin.py, implement a program that:
# Expects the user to specify as a command-line argument the number of Bitcoins, n, that they would like to buy. If that argument cannot be converted to a float, the program should exit via sys.exit with an error message.
# Queries the API for the CoinDesk Bitcoin Price Index at https://api.coindesk.com/v1/bpi/currentprice.json, which returns a JSON object, among whose nested keys is the current price of Bitcoin as a float. Be sure to catch any exceptions
# try:
#     ...
# except requests.RequestException:
#     ...


import requests
import sys

# import json

response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
# print(json.dumps(response.json(), indent=2))
obj = response.json()
bit_price = obj["bpi"]["USD"]["rate_float"]

try:
    if len(sys.argv) < 2:
        print("Missing Command-line argument")
        sys.exit(1)

    user_input = float(sys.argv[1])

except (ValueError, requests.RequestException):
    print("Command-Line argument is not a number")
    sys.exit(1)


def convert(n):
    n = n * bit_price
    return n


result = convert(user_input)
print(f"${result:,.4f}")
