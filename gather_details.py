# -*- coding: utf-8 -*-
import scrapy
import re
from tld import get_tld
import csv
import pandas as pd

# Import .csv file of dental leads into Python
df = pd.read_csv(r'oral-surgeon-leads.csv')
df["Email"] = "N/A"
print(df)

class GatherDetailsSpider(scrapy.Spider):
    name = 'gather_details'
    greedy = True
    email_regex = re.compile(r"[-.a-z]+@[^@\s\.]+\.[.a-z]{2,3}")
    forbidden_keys = ['tel:', 'mailto:', '.jpg', '.pdf', '.png']
    
    def __init__(self, domain, **kwargs):
        self.allowed_domains = [f'{domain}']
        self.start_urls = [f'https://{domain}']
        super().__init__(**kwargs)

    def parse(self, response):
        try:
            html = response.body.decode('utf-8')
        except UnicodeDecodeError:
            return
        emails = []
        phones = []
        # Find mailto's
        mailtos = response.xpath("//a[starts-with(@href, 'mailto')]/@href").getall()
        tels = response.xpath("//a[starts-with(@href, 'tel:')]/@href").getall()
        phones += [tel.replace("tel:", "") for tel in tels]
        emails = [mail.replace('mailto:', '') for mail in mailtos]
        body_emails = self.email_regex.findall(html)
        emails += [email for email in body_emails if \
            get_tld('https://' + email.split('@')[-1], fail_silently=True)]
        yield {
            'emails': list(set(emails)),
            'phones': list(set(phones)),
            'page': response.request.url
        }
        if self.greedy:
            links = response.xpath("//a/@href").getall()
            # If there are external links, scrapy will block them
            # because of the allowed_domains setting
            for link in links:
                skip = False
                for key in self.forbidden_keys: 
                    if key in link:
                        skip = True
                        break
                if skip:
                    continue
                try:
                    yield scrapy.Request(link, callback=self.parse)
                except ValueError:
                    try:
                        yield response.follow(link, callback=self.parse)
                    except:
                        pass


info = GatherDetailsSpider("http://www.speedbracer.com")