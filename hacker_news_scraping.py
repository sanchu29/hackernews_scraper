import requests
import io
from bs4 import BeautifulSoup
import time
import csv

results=[]
number_of_pages=10
url='https://thehackernews.com/'

for page in range(number_of_pages):

    html=requests.get(url)
    content=BeautifulSoup(html.text,'html.parser')
    titles=[title.text for title in content.findAll('h2',{'class':'home-title'})]
    links=[link['href'] for link in content.findAll('a',{'class':'story-link'})]
    dates=[[inner_tag for inner_tag in outer_tag][1] for outer_tag in content.findAll('div',{'class':'item-label'})]
    authors=[[inner_tag for inner_tag in outer_tag][2].text.strip()[1:] for outer_tag in content.findAll('div',{'class':'item-label'})]
    descriptions=[description.text.strip() for description in content.findAll('div',{'class':'home-desc'})]
    next_page=content.find('a',{'class':'blog-pager-older-link-mobile'})['href']

    for i in range(len(titles)):
        item={
            'title':titles[i],
            'link':links[i],
            'date':dates[i],
            'author':authors[i],
            'description':descriptions[i],
            'next_page':next_page
        }
        results.append(item)

    print(f'Scraped page number {page+1}')
    url=next_page

with io.open('news.csv','a',encoding="utf-8") as csv_file:
    writer=csv.DictWriter(csv_file,fieldnames=results[0].keys())
    writer.writeheader()

    for row in results:
        writer.writerow(row)

