#!/usr/bin/env python3
"""
Professional Web Scraper Pro v1.0
Author: Biswajit
Features: Error handling, retry, progress bar, logging, rate limiting, CLI args
"""

import requests
import csv
import time
import logging
import argparse
from datetime import datetime
from typing import Optional

# ==================== CONFIGURATION ====================
DEFAULT_URL = "https://fakestoreapi.com/products"
DEFAULT_OUTPUT = "products.csv"
DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3
DEFAULT_DELAY = 1  # seconds between requests

# ==================== LOGGING SETUP ====================
def setup_logging(log_file: str = "scraper.log"):
    """Setup logging to both file and console"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# ==================== PROGRESS BAR ====================
def progress_bar(current: int, total: int, bar_length: int = 40):
    """Display a simple progress bar"""
    percent = current / total
    filled = int(bar_length * percent)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"\r📊 Progress: |{bar}| {current}/{total} ({percent*100:.1f}%)", end="", flush=True)

# ==================== API FETCHER ====================
def fetch_data(url: str, timeout: int = DEFAULT_TIMEOUT, retries: int = DEFAULT_RETRIES, delay: float = DEFAULT_DELAY) -> Optional[list]:
    """
    Fetch data from API with retry logic and error handling
    
    Args:
        url: API endpoint URL
        timeout: Request timeout in seconds
        retries: Number of retry attempts
        delay: Delay between retries
    
    Returns:
        List of products or None if failed
    """
    headers = {
        "User-Agent": "WebScraperPro/1.0",
        "Accept": "application/json"
    }
    
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"🌐 Fetching data (Attempt {attempt}/{retries})...")
            
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()  # Raises exception for 4xx/5xx
            
            data = response.json()
            logger.info(f"✅ Successfully fetched {len(data)} items")
            return data
            
        except requests.exceptions.Timeout:
            logger.warning(f"⏱️ Timeout error (Attempt {attempt}/{retries})")
            
        except requests.exceptions.ConnectionError:
            logger.warning(f"🔌 Connection error (Attempt {attempt}/{retries})")
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"❌ HTTP Error: {e}")
            return None
            
        except requests.exceptions.JSONDecodeError:
            logger.error("❌ Invalid JSON response")
            return None
            
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            return None
        
        if attempt < retries:
            logger.info(f"⏳ Waiting {delay}s before retry...")
            time.sleep(delay)
    
    logger.error("❌ All retry attempts failed")
    return None

# ==================== DATA VALIDATION ====================
def validate_product(product: dict) -> dict:
    """
    Validate and clean product data
    
    Args:
        product: Raw product dictionary
    
    Returns:
        Cleaned product dictionary
    """
    return {
        "title": str(product.get("title", "N/A")).strip()[:100],  # Max 100 chars
        "price": float(product.get("price", 0)),
        "category": str(product.get("category", "N/A")).strip(),
        "description": str(product.get("description", "N/A")).strip()[:200],
        "image": str(product.get("image", "N/A")).strip(),
        "rating": product.get("rating", {}).get("rate", 0),
        "rating_count": product.get("rating", {}).get("count", 0)
    }

# ==================== CSV WRITER ====================
def save_to_csv(products: list, output_file: str) -> bool:
    """
    Save products to CSV file
    
    Args:
        products: List of product dictionaries
        output_file: Output CSV filename
    
    Returns:
        True if successful, False otherwise
    """
    if not products:
        logger.error("❌ No products to save")
        return False
    
    try:
        headers = ["Title", "Price", "Category", "Description", "Image URL", "Rating", "Rating Count"]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            
            for i, product in enumerate(products):
                clean_product = validate_product(product)
                writer.writerow([
                    clean_product["title"],
                    f"${clean_product['price']:.2f}",
                    clean_product["category"],
                    clean_product["description"],
                    clean_product["image"],
                    clean_product["rating"],
                    clean_product["rating_count"]
                ])
                progress_bar(i + 1, len(products))
        
        print()  # New line after progress bar
        logger.info(f"💾 Saved {len(products)} products to {output_file}")
        return True
        
    except PermissionError:
        logger.error(f"❌ Permission denied: Cannot write to {output_file}")
        return False
    except Exception as e:
        logger.error(f"❌ Error saving CSV: {e}")
        return False

# ==================== STATISTICS ====================
def show_statistics(products: list):
    """Display statistics about scraped data"""
    if not products:
        return
    
    prices = [p.get("price", 0) for p in products]
    categories = {}
    
    for p in products:
        cat = p.get("category", "Unknown")
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n" + "="*50)
    print("📈 SCRAPING STATISTICS")
    print("="*50)
    print(f"📦 Total Products: {len(products)}")
    print(f"💰 Price Range: ${min(prices):.2f} - ${max(prices):.2f}")
    print(f"💵 Average Price: ${sum(prices)/len(prices):.2f}")
    print(f"📂 Categories:")
    for cat, count in categories.items():
        print(f"   • {cat}: {count} items")
    print("="*50)

# ==================== MAIN FUNCTION ====================
def main():
    """Main entry point with CLI argument parsing"""
    parser = argparse.ArgumentParser(
        description="🕷️ Professional Web Scraper Pro v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python web_scraper_pro.py
  python web_scraper_pro.py --output data.csv
  python web_scraper_pro.py --url https://api.example.com/products --timeout 60
  python web_scraper_pro.py --retries 5 --delay 2
        """
    )
    
    parser.add_argument("-u", "--url", default=DEFAULT_URL, help="API URL to scrape")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT, help="Output CSV filename")
    parser.add_argument("-t", "--timeout", type=int, default=DEFAULT_TIMEOUT, help="Request timeout (seconds)")
    parser.add_argument("-r", "--retries", type=int, default=DEFAULT_RETRIES, help="Number of retry attempts")
    parser.add_argument("-d", "--delay", type=float, default=DEFAULT_DELAY, help="Delay between retries (seconds)")
    parser.add_argument("--no-stats", action="store_true", help="Disable statistics display")
    
    args = parser.parse_args()
    
    # Banner
    print("""
╔═══════════════════════════════════════════════════════╗
║         🕷️  WEB SCRAPER PRO v1.0  🕷️                 ║
║         Professional Data Extraction Tool             ║
╚═══════════════════════════════════════════════════════╝
    """)
    
    start_time = datetime.now()
    logger.info(f"🚀 Starting scraper at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"🎯 Target URL: {args.url}")
    
    # Fetch data
    products = fetch_data(
        url=args.url,
        timeout=args.timeout,
        retries=args.retries,
        delay=args.delay
    )
    
    if products:
        # Save to CSV
        if save_to_csv(products, args.output):
            # Show statistics
            if not args.no_stats:
                show_statistics(products)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.info(f"⏱️ Total time: {duration:.2f} seconds")
            logger.info("🎉 Scraping completed successfully!")
            return 0
    
    logger.error("❌ Scraping failed!")
    return 1

# ==================== ENTRY POINT ====================
if __name__ == "__main__":
    exit(main())
