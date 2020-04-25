import arrow


class Paste:
    def __init__(self, author, title, content, date):
        self.author = author
        self.title = title
        self.date = date
        self.content = content

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        if(author.lower() == "a guest"):
            author = ""
        self._author = author

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if(title.lower() == "untitled"):
            title = ""
        self._title = title

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content.rstrip()

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        date_arrow = arrow.get(date, "Do of MMMM YYYY hh:mm:ss A")
        self._date = date_arrow.format('YYYY-MM-DD HH:mm:ss ZZ')
