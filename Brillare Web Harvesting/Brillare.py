import requests
from bs4 import BeautifulSoup
import re
import time


base_url = 'https://www.brillare.co.in/collections/all?page={}'


header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

all_products = []

for page_num in range(1, 10):
    url = base_url.format(page_num)
    page = requests.get(url, headers=header)
    
  
    if page.status_code != 200:
        print(f"Skipping page {page_num}, status code: {page.status_code}")
        break
    
    soup = BeautifulSoup(page.content, "html.parser")
    

    product_names = [tag.get_text(strip=True) for tag in soup.find_all("a", class_="card-information__text h4 collection_titlecls")]

 
    price_tags = soup.find_all("span", class_=re.compile(r"price|amount|rs|₹", re.IGNORECASE))
    product_prices = [tag.get_text(strip=True) for tag in price_tags]


    product_urls = ["https://www.brillare.co.in" + tag['href'] for tag in soup.find_all("a", class_="card-information__text h4 collection_titlecls")]


    for name, price, url in zip(product_names, product_prices, product_urls):
        all_products.append({"name": name, "price": price, "url": url})

    print(f"Scraped page {page_num}")
    
    
    time.sleep(2)


print(f"Total products scraped: {len(all_products)}")
for product in all_products:
    print(product)
