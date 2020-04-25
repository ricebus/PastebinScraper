# PastebinScraper
Scrape pastes from pastebin.com

# Run (from project dir)
pip install -r requirements.txt
python main.py

# Docker (from project dir)
docker build -t python-pastebin-scraper .
docker pull mongo:3-xenial