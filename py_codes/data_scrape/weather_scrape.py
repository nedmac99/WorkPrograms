import requests
from bs4 import BeautifulSoup

url = "https://forecast.weather.gov/MapClick.php?textField1=34.257&textField2=-85.1647"

response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, 'html.parser')

current_conditions = soup.find(id="current_conditions-summary")

if current_conditions:
    temp = current_conditions.find(class_="myforecast-current-lrg")
    desc = current_conditions.find(class_="myforecast-current")
    if temp and desc:
        print("Temperature in Rome, Ga:", temp.text.strip())
        print("Description:", desc.text.strip())
    else:
        print("Could not find temperature or description.")
else:
    print("Could not find current conditions.")