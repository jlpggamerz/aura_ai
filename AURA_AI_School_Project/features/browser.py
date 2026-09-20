import webbrowser
from urllib.parse import quote_plus

class Browser:
    def open(self, url):
        webbrowser.open(url)

    def search(self, query):
        url = "https://www.google.com/search?q=" + quote_plus(query)
        self.open(url)
