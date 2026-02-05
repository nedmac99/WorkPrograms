from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Start browser
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Load page
driver.get("https://eldenring.wiki.fextralife.com/Limgrave")
time.sleep(5)

# Get rendered HTML
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# Function to find the heading with specific text
def is_heading_with_text(tag):
    return tag.name in ["h2", "h3", "h4"] and "Locations" in tag.get_text()

# Step 1: Find the heading
heading = soup.find(is_heading_with_text)

# Step 2: First list after heading
if heading:
    first_list = heading.find_next("ul")
else:
    first_list = None

# Step 3: Second list after the first one
if first_list:
    second_list = first_list.find_next("ul")
else:
    second_list = None

# Extract items
if second_list:
    items = [li.get_text(strip=True) for li in second_list.find_all("li")]
    print(items)
else:
    print("Second list not found.")