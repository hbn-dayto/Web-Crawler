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
# url = 'https://www.yellowpages.com/search?search_terms=Cheerleading+&geo_location_terms=Covina%2C+CA'
business_names = []
business_websites = []

# Scrapes the first 50 pages for cosmetic dentists in san dimas, ca
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

  
# Create csv file after the for loop is finished is finished iterating 
df = pd.DataFrame({"Business Name": business_names,
                   "Website": business_websites
                   })

# Clean dataset and filter out leads with no website
newdf = df[df["Website"]!="N/A"]
# newdf.to_csv('dentist_list_cleaned.csv', index=False)
# newdf.to_csv('cheerleads.csv', index=False)
newdf.to_csv('oral-surgeon-leads.csv', index=False)
no_website = df[df["Website"]=="N/A"]
no_website.to_csv('no_website.csv', index=False)


df = pd.read_csv (r'dentist_list_cleaned.csv')
df["Email"] = "N/A"
df = df.iloc[0:50]

df["Email"] = df.apply(lambda x: webcrawler.EmailCrawler(x["Website"], axis=1))





