# Import packages

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import requests
import re
from urllib.parse import urljoin

########################################################################################################
# Function to scrape the data from the website
# 1. Get links to the pages with the data

# Use the urljoin function from Python's urllib.parse module to join the base URL with the relative URLs found in the href attributes.

def get_product_links(base_url, url):     
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    product_links = set () # Initiate an empty set to store product links. A set is an unordered collection of unique elements, compared to the list
    
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and "/fr-fr/products/" in href:  # Check if href contains "/fr-fr/products/"
            full_url = urljoin(base_url, href)
            product_links.add(full_url) # Add the full URL to the set
            
    return product_links

# 2. Get the data from the pages
def get_product_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    script = soup.find('script', string=re.compile('dataLayer')) # Using "string" instead of "text"
    json_text = re.search(r'dataLayer\s*=\s*(\[.*?\]);', script.string, flags=re.DOTALL | re.MULTILINE).group(1)

    data = json.loads(json_text)

    # Extract product information
    product_info = data[1]['ecommerce']['detail']['products'][0]
    name = product_info['name']
    id = product_info['id']
    price = product_info['price']
    gender = product_info['gender']

    # Convert the dictionary into dataframe
    #product_info = pd.DataFrame([product_info])

    return product_info

# 3. Main function to scrape the data
def get_all_product_info(base_url, url):
    # List to store product information
    product_info_list = []

    # Get product information for each product
    
    product_links = get_product_links(base_url, url)
    for link in product_links:
        product_info = get_product_info(link)
        product_info_list.append(product_info)

    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(product_info_list)

    return df

