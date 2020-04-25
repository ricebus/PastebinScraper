import requests
from bs4 import BeautifulSoup as bs
from paste import Paste
import json

base_url = "https://pastebin.com"
chrome_mock_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",
    "Cache-Control": "max-age=0"
}

s = requests.session()  # session
s.headers.update(chrome_mock_headers)
s.max_redirects = 3

html = s.get(base_url)
soup = bs(html.text, 'html.parser')
paste_list = soup.find_all("ul", "right_menu")[0]
li_tags_list = paste_list.li
for li in li_tags_list.next_siblings:
    link = li.a.get("href")
    #link = "/X21hFx99"
    html = s.get(base_url + link)
    soup = bs(html.text, 'html.parser')
    info_box = soup.find_all("div", "paste_box_info")[0]
    info_line = info_box.find_all("div", "paste_box_line2")[0]
    paste_box = soup.find_all("div", "textarea_border")[0]
    title = info_box.find_all("div", "paste_box_line1")[0].text
    author = info_line.a.text
    date = info_line.span.get("title")
    content = paste_box.textarea.text
    obj = Paste(author,title,content,date)
    print(json.dumps(obj.__dict__))

