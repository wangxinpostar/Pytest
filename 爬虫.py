import requests
from lxml import etree

class Douban:
    def __init__(self):
        self.URL = 'https://movie.douban.com/top250'
        self.starnum = []
        for start_num in range(0, 226, 25):
            self.starnum.append(start_num)
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.43'}

    def get_top250(self):
        for start in self.starnum:
            start = str(start)
            respone = requests.get(
                self.URL, params={'start': start}, headers=self.header)
            text = respone.text
            content = respone.content
            html = etree.HTML(text)
            for i in range(25):
                i=str(i)
                title = "".join(html.xpath(
                    "/html/body/div[3]/div[1]/div/div[1]/ol/li["+i+"]/div/div[2]/div[1]/a/span[1]/text()"))
                score = "".join(html.xpath(
                    "/html/body/div[3]/div[1]/div/div[1]/ol/li["+i+"]/div/div[2]/div[2]/div/span[2]/text()"))
                scoret = "".join(html.xpath(
                    "/html/body/div[3]/div[1]/div/div[1]/ol/li["+i+"]/div/div[2]/div[2]/div/span[4]/text()"))
                director = "".join(html.xpath(
                    "/html/body/div[3]/div[1]/div/div[1]/ol/li["+i+"]/div/div[2]/div[2]/p[1]/text()[1]"))
                print(title, score, scoret, director, "\n")

if __name__ == "__main__":
    cls = Douban()
    cls.get_top250()
