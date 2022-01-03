from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
import requests.exceptions

import webcrawler

from urllib.parse import urlsplit, urljoin
from lxml import html
import sys
import csv

url = 'https://www.yellowpages.com/san-dimas-ca/oral-surgeon?page='
business_names = []
business_websites = []

for page in range(1,50):
    print("page is: ", page)
    response = requests.get(url + str(page))
    print("URL IS:", response)
    soup= BeautifulSoup(response.text,'html.parser')
    # def extract_info(source):   

    results = soup.find_all('div', class_="result")
    for result in results:
        business_name = result.find('a', class_="business-name").text
        business_names.append(business_name)
        try:
            # website_url = result.find('a', class_="track-visit-website")
            links = result.find('div', class_="links")
            website_link = links.find('a', class_="track-visit-website")
            business_websites.append(website_link.get('href'))
        except:
            business_websites.append('N/A')


df = pd.DataFrame({"Business Name": business_names,
                   "Website": business_websites
                   })

# Clean dataset and filter out leads with no website
newdf = df[df["Website"]!="N/A"]

newdf.to_csv('oral-surgeon-leads.csv', index=False)

# df = pd.read_csv (r'dentist_list_cleaned.csv')
# df["Email"] = "N/A"
# df = df.iloc[0:50]

# df["Email"] = df.apply(lambda x: webcrawler.EmailCrawler(x["Website"], axis=1))





