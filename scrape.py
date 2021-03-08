import logging
import sqlite3
from os import environ
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime


# Configurable Settings
skus_to_ignore = [224279, 963264, 229401, 388249]
store_id = '045'
nvidia_gpu_url = 'https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&N=4294966937+4294821460'
db_file = 'data.db'


def get_soup(url, store_id):
  ''' Open the page and parse the HTML using BeautifulSoup '''
  # Add the store id to the end of the url
  full_url = url + '&myStore=true&storeid=' + store_id
  page = urlopen(full_url)
  check_time = int(datetime.now().timestamp())
  html = page.read().decode("utf-8")
  soup = BeautifulSoup(html, "html.parser")

  return (check_time, soup)


def get_products(soup, store_id, check_time):
  ''' Search the soup and return product data '''
  products = []
  # Find the products and get SKU, Name, Price, Stock and Availability
  products_soup = soup.find_all("li", {"class": "product_wrapper"})
  for product_soup in products_soup:
    product = {}
    sku_soup = product_soup.find("p", {"class", "sku"}).get_text(strip=True)
    sku = int(sku_soup[4::])
    name = product_soup.find("h2").get_text(strip=True)
    stock_text = product_soup.find("div", {"class", "stock"}).text.strip()
    stock = int(stock_text.replace(' in stock','').replace('+', ''))
    price_soup = product_soup.find("div", {"class", "price"}).get_text(strip=True)
    price = float(price_soup[1::])
    availability = product_soup.find("div", {"class", "instore"}).get_text(strip=True)
    # Assemble available data to dict
    product = {
        'datetime': check_time,
        'sku': sku,
        'name': name,
        'store': store_id,
        'stock': stock,
        'availability': availability
        }
    logging.debug(f"Product: {product}")
    products.append(product)

  return products
  

def send_alerts(products)
  ''' Send alert messages for products not in ignore list '''
  for product in products:
    sku = product['sku']
    # Check if we want to ignore this product
    if sku in skus_to_ignore:
      logging.debug(f"Ignoring SKU {sku}")
      continue
    else:
      name = product['name']
      logging.info(f"Found new SKU {sku}! - {name}")

  return true


def log_data(products):
  ''' Save data for trend charts '''
  conn = connect_database(db_file)
  with conn:
    insert_bulk_data(conn, products)
  return True


def connect_database(db_file):
  ''' Atempt to open connection to sqlite3 db '''
  conn = None
  try:
    conn = sqlite3.connect(db_file)
  except Error as error:
    logging.Error(error)

  return conn


def main():
  ''' Do all the stuff '''
  check_time, soup = get_soup(nvidia_gpu_url, store_id)
  products = get_products(soup, store_id, check_time)
  send_alerts(products)


if __name__ == '__main__':
  # Initialize logging
  LOGLEVEL = environ.get('LOGLEVEL', 'DEBUG').upper()
  logging.basicConfig(level=LOGLEVEL)

  main()
