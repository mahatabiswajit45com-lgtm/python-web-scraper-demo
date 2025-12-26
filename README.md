# 🕷️ Web Scraper Pro v1.0

A production-ready Python web scraper built for reliability and performance.

## ✨ Features

- **Smart Retry Logic** - Auto-retries failed requests with configurable delays
- **Error Handling** - Handles timeouts, connection errors, and invalid responses
- **Progress Tracking** - Real-time progress bar during scraping
- **Data Validation** - Cleans and validates data before export
- **Logging System** - Logs to both console and file for debugging
- **CLI Support** - Fully customizable via command-line arguments
- **Statistics** - Shows price range, categories, and item counts

## 🚀 Quick Start

```bash
pip install requests
python web_scraper_pro.py
```

## 📋 Usage Examples

```bash
# Basic usage
python web_scraper_pro.py

# Custom output file
python web_scraper_pro.py -o products_2024.csv

# Custom API endpoint
python web_scraper_pro.py -u https://api.example.com/data

# Increase retries and timeout
python web_scraper_pro.py --retries 5 --timeout 60 --delay 2
```

## ⚙️ CLI Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--url` | `-u` | fakestoreapi.com | API endpoint URL |
| `--output` | `-o` | products.csv | Output filename |
| `--timeout` | `-t` | 30 | Request timeout (seconds) |
| `--retries` | `-r` | 3 | Retry attempts |
| `--delay` | `-d` | 1 | Delay between retries |
| `--no-stats` | | False | Hide statistics |

## 📁 Output

The scraper exports data to CSV with these columns:
- Title, Price, Category, Description, Image URL, Rating, Rating Count

## 📝 Logs

All activity is logged to `scraper.log` with timestamps.

## 🛠️ Tech Stack

- Python 3.x
- Requests library
- CSV module
- Argparse for CLI

## 👨‍💻 Author

**Biswajit** - Python Developer | Automation Specialist

---

*Built with ❤️ for data extraction tasks*
