import urllib.request
from html_table_parser.parser import HTMLTableParser
import pandas as pd


class InterestRate:
    def url_get_contents(self,url):
        req = urllib.request.Request(url=url)
        f = urllib.request.urlopen(req)
        return f.read()

    def get_rate(self):
        xhtml = self.url_get_contents(
            'https://timo.vn/tai-khoan-tiet-kiem/lai-suat-gui-tiet-kiem-ngan-hang-nao-cao-nhat/').decode(
            'utf-8')

        p = HTMLTableParser()
        p.feed(xhtml)

        deposit_rate = pd.DataFrame(p.tables[0])
        deposit_rate.columns = deposit_rate.iloc[0]
        deposit_rate = deposit_rate[1:]
        deposit_rate.head()

        return deposit_rate

df = InterestRate()
print(df.get_rate())