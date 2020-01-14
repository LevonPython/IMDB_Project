import init_sql as db
from bs4 import BeautifulSoup
import requests


class Source:
    def __init__(self, url):
        self.db = db.DataBase('data')
        self.db.create_table()
        self.source = requests.get(url).text

    def get_ids(self):

        while True:

            soup = BeautifulSoup(self.source, 'lxml')

            for film in soup.find_all('div', class_='lister-item-content'):
                title = film.h3.a.text
                idx = film.h3.a['href'].split('/')[2][2:]
                self.db.insert_mids(idx, title)
            self.db.conn.commit()
            print('dasdjka')

            # try:
            #     nextpg = f"https://www.imdb.com{soup.find('a', class_='lister-page-next next-page')['href']}"
            #     self.source = requests.get(nextpg).text
            # except:
            #     break


if __name__ == '__main__':
    source = Source('https://www.imdb.com/search/title/?title_type=feature&release_date=1927-01-01,2019-12-31&user_rating=1.0,&sort=year,asc&count=250')
    source.get_ids()
