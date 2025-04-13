from scraper import MarketplaceScraper
import time
import schedule

def run_scraper():
    scraper = MarketplaceScraper()
    
    # Define the marketplaces to scrape
    marketplaces = {
        'craigslist': 'https://sfbay.craigslist.org/search/sss?query=swap'
    }
    
    for name, url in marketplaces.items():
        try:
            print(f"[INFO] Scraping {name}...")
            items = scraper.scrape_marketplace(url, name)

            if items:
                print(f"[SUCCESS] Found {len(items)} items from {name}")
                scraper.save_to_database(items)
            else:
                print(f"[WARN] No items found for {name}")
        except Exception as e:
            print(f"[ERROR] Failed to scrape {name}: {e}")
    
    try:
        scraper.export_to_json()
        print("[INFO] Exported data to JSON successfully")
    except Exception as e:
        print(f"[ERROR] Failed to export JSON: {e}")

def main():
    print("[STARTUP] Starting marketplace scraper...")

    # Run immediately
    run_scraper()

    # Schedule to run every 6 hours
    schedule.every(6).hours.do(run_scraper)

    print("[SCHEDULER] Scraper scheduled to run every 6 hours.")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()