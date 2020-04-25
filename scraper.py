import requests
from bs4 import BeautifulSoup as bs
from paste import Paste


class Scraper:
    def __init__(self, base_url="https://pastebin.com", headers=None):
        self.base_url = base_url
        chrome_mock_headers = {
            "User-Agent":   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/81.0.4044.113 Safari/537.36",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "Cache-Control": "max-age=0"
        }

        self.s = requests.session()
        if headers is None:
            self.s.headers.update(chrome_mock_headers)
        else:
            self.s.headers.update(headers)

    def run(self):
        html = self.s.get(self.base_url)
        if html.text.find("Pastebin.com has blocked your IP") != -1:
            raise ConnectionRefusedError("Pastebin.com has blocked your IP")
        return self.parse_main_page(html.text)

    def parse_main_page(self, html):
        soup = bs(html, 'html.parser')
        paste_list = soup.find_all("ul", "right_menu")[0]
        li_tags_list = paste_list.li
        pastes = []
        for li in li_tags_list.next_siblings:
            link = li.a.get("href")
            page_html = self.s.get(self.base_url + link)
            print(self.base_url + link)
            paste = self.parse_paste_page(page_html.text, link.strip("/"))
            if paste is not None:
                pastes.append(paste)

        return pastes

    def parse_paste_page(self, html, id):
        soup = bs(html, 'html.parser')
        removed = True if soup.find_all("div", "content_title")[0] \
                              .text.find("removed") != -1 \
            else False
        if removed:
            return None

        info_box = soup.find_all("div", "paste_box_info")[0]
        info_line = info_box.find_all("div", "paste_box_line2")[0]
        paste_box = soup.find_all("div", "textarea_border")[0]
        title = info_box.find_all("div", "paste_box_line1")[0].text
        date = info_line.span.get("title")
        content = paste_box.textarea.text
        author = info_line.a.text \
            if info_line.text.lower().find("guest") == -1 \
            else "guest"
        return Paste(id, author, title, content, date)
