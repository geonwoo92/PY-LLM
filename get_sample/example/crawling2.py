
from urllib.request import urlopen

from bs4 import BeautifulSoup
import pandas as pd


class ScrapBugs:

    def __init__(self) -> None:
        pass

    def scrap(self) -> {}:
        print('Scrap bugs!')
        url = ('https://music.bugs.co.kr/chart/track/realtime/total?')
        html_doc = urlopen(url)
        soup = BeautifulSoup(html_doc, 'lxml')
        list1 = self.find_music(soup, 'title')
        list2 = self.find_music(soup, 'artist')
        a = [i if i == 0 or i == 0 else i for i in range(1)]
        b = [i if i == 0 or i == 0 else i for i in []]
        c = [(i, j) for i, j in enumerate([])]
        d = {i: j for i, j in zip(list1, list2)}
        l = [i+j for i, j in zip(list1, list2)]
        l2 = list(zip(list1, list2))
        d1 = dict(zip(list1, list2))
        print(d1)
        return d

    @staticmethod
    def find_music(soup: BeautifulSoup, classname):
        list = soup.find_all('p', {'class': classname})

        return [i.get_text() for i in list]


if __name__ == '__main__':
    bugs = ScrapBugs()
    bugs.scrap()
    data = bugs.scrap()

 # 데이터프레임으로 변환
    df = pd.DataFrame(list(data.items()), columns=['Title', 'Artist'])

    # CSV 파일로 저장
    df.to_csv('bugs_chart.csv', index=False)
    print("CSV 파일 저장 완료: bugs_chart.csv")
