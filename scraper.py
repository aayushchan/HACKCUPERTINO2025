import sqlite3
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

DB_PATH = 'marketplaces.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  type TEXT,
                  location TEXT,
                  description TEXT,
                  price TEXT,
                  link TEXT,
                  source TEXT,
                  dateAdded TEXT)''')
    conn.commit()
    conn.close()

def save_to_database(items):
    if not items:
        return
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for item in items:
        c.execute('''INSERT INTO items 
                     (name, type, location, description, price, link, source, dateAdded)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  (item['name'], item['type'], item['location'], 
                   item['description'], item['price'], item['link'], 
                   item['source'], item['dateAdded']))
    conn.commit()
    conn.close()

def export_to_json():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM items')
    rows = c.fetchall()

    items = [{
        'id': row[0],
        'name': row[1],
        'type': row[2],
        'location': row[3],
        'description': row[4],
        'price': row[5],
        'link': row[6],
        'source': row[7],
        'dateAdded': row[8]
    } for row in rows]

    with open('marketplace_items.json', 'w') as f:
        json.dump(items, f, indent=4)

    print(f"Exported {len(items)} items to marketplace_items.json")
    conn.close()

def scrape_marketplace(url, marketplace_name):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        response = requests.get(url, headers=headers, timeout=10)
        items = []

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            if marketplace_name == 'craigslist':
                items = scrape_craigslist(soup)
            elif marketplace_name == 'facebook':
                items = scrape_facebook(soup)
            elif marketplace_name == 'offerup':
                items = scrape_offerup(soup)

            for item in items:
                item['source'] = marketplace_name
                item['dateAdded'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return items
    except Exception as e:
        print(f"Error scraping {marketplace_name}: {e}")
        return []

def scrape_craigslist(soup):
    items = []
    listings = soup.find_all('li', class_='cl-static-search-result')

    for listing in listings:
        try:
            title_element = listing.find('div', class_='title')
            price_element = listing.find('div', class_='price')
            meta_element = listing.find('div', class_='meta')
            link_element = listing.find('a', class_='posting-title')

            if title_element and link_element:
                items.append({
                    'name': title_element.text.strip(),
                    'type': 'Swap',
                    'location': meta_element.text.strip() if meta_element else 'SF Bay Area',
                    'description': 'Click for details',
                    'price': price_element.text.strip() if price_element else 'Price not listed',
                    'link': link_element['href']
                })
        except Exception as e:
            print(f"Error parsing Craigslist listing: {e}")
            continue

    print(f"Found {len(items)} items on Craigslist")
    return items

def scrape_facebook(soup):
    items = []
    listings = soup.find_all('div', {'class': 'kbiprv82'})

    for listing in listings[:10]:
        try:
            title = listing.find('span', {'class': 'a8c37x1j'})
            price = listing.find('span', {'class': 'oi732d6d'})

            items.append({
                'name': title.text if title else 'No Title',
                'type': 'Swap',
                'location': 'Local',
                'description': 'View on Facebook',
                'price': price.text if price else 'Price not listed',
                'link': 'https://www.facebook.com/marketplace/'
            })
        except Exception as e:
            print(f"Error parsing Facebook listing: {e}")
            continue

    return items

def scrape_offerup(soup):
    items = []
    listings = soup.find_all('div', {'class': '_109rpto'})

    for listing in listings[:10]:
        try:
            title = listing.find('span', {'class': '_s3g03e4'})
            price = listing.find('span', {'class': '_ckr3pn'})

            items.append({
                'name': title.text if title else 'No Title',
                'type': 'Swap',
                'location': 'Local',
                'description': 'View on OfferUp',
                'price': price.text if price else 'Price not listed',
                'link': 'https://offerup.com'
            })
        except Exception as e:
            print(f"Error parsing OfferUp listing: {e}")
            continue

    return items

# Example usage:
if __name__ == '__main__':
    init_db()
    craigslist_items = scrape_marketplace('https://sfbay.craigslist.org/search/sss?query=swap', 'craigslist')
    save_to_database(craigslist_items)
    export_to_json()