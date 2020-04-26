# PastebinScraper
Scrape pastes from pastebin.com

# Run (from project dir)
```
pip install -r requirements.txt
export SCRAPER_MODE="db"
export SCRAPER_CONN_STRING="mongodb://127.0.0.1:27017/"
python main.py
```
# Docker (from project dir)
```
docker build -t python-pastebin-scraper:latest .
docker pull mongo:3-xenial
docker run -d python-pastebin-scraper:latest \
-e SCRAPER_MODE="db" \
-e SCRAPER_CONN_STRING="mongodb://127.0.0.1:27017/" \
--name scraper 
docker run -d -p 27017-27019:27017-27019 \
-v //c/mongodb-data://data/db \
--name mongodb mongo
```

# NOTE
file mode only dumps data