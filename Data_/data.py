import init_sql as db
import modify as mod
from bs4 import BeautifulSoup
import requests
import re
# import pandas as pd


# data = pd.read_csv('id_title.csv')


class Scrapper:
    def __init__(self, base_url, idx):
        self.movie = {}
        self.person = {}
        self.credits = []
        self.db = db.DataBase('data')
        self.db.create_table()
        self.page = BeautifulSoup(requests.get(
            base_url.format(f'{idx}'.rjust(12, '0'))).content, 'lxml')

    def details(self, idx):
        # image
        try:
            self.movie['image'] = self.page.select_one(
                'div#title-overview-widget div.poster > a > img').get('src')
        except:
            self.movie['image'] = None

        # details
        details = self.page.select('div#titleDetails > div')
        for detail in details:
            link_tag = detail.select('a')
            char = mod.var_name(detail.text)
            # if we have linked char we can get text
            if link_tag not in ([], None) and link_tag[0].text != 'See more':
                if len(link_tag) > 1 and char != 'show_more_on_imdbpro_»':
                    ab = [t.text.strip()
                          for t in link_tag if t.text.strip() != 'See more']
                    if len(ab) != 1:
                        self.movie[char] = ab
                    else:
                        self.movie[char] = ab[0].strip()
                if len(link_tag) == 1 and char != 'show_more_on_imdbpro_»':
                    self.movie[char] = link_tag[0].text.strip()
            else:
                self.movie[char] = mod.var_value(detail.text)

        try:
            self.movie['runtime'] = int(self.movie.get('runtime').split()[0])
        except:
            self.movie['runtime'] = None
        if isinstance(self.movie.get('color'), list):
            self.movie['color'] = ', '.join(self.movie.get('color'))
        else:
            self.movie['color'] = self.movie.get('color')

        self.db.insert_details(idx, self.movie)

    def companies(self, idx):
        if isinstance(self.movie.get('production_co'), list):
            for company in self.movie.get('production_co'):
                self.db.insert_companies(idx, company)
        else:
            self.db.insert_companies(idx, self.movie.get('production_co'))

    def countries(self, idx):
        if isinstance(self.movie.get('country'), list):
            for country in self.movie.get('country'):
                self.db.insert_countries(idx, country)

        else:
            self.db.insert_countries(idx, self.movie.get('country'))

    def languages(self, idx):
        if isinstance(self.movie.get('language'), list):
            for language in self.movie.get('language'):
                self.db.insert_languages(idx, language)
        else:
            self.db.insert_languages(idx, self.movie.get('language'))

    def genres(self, idx):
        # genres
        storyline = self.page.select('div#titleStoryLine > div > h4')
        for inline in storyline:
            if inline.text == 'Genres:':
                genres = inline.findNextSiblings('a')
                if len(genres) > 1:
                    self.movie['genres'] = [i.text.strip() for i in genres]
                else:
                    self.movie['genres'] = genres[0].text.strip()

        if isinstance(self.movie.get('genres'), list):
            for genre in self.movie.get('genres'):
                self.db.insert_genres(idx, genre)

        else:
            self.db.insert_genres(idx, self.movie.get('genres'))

    def ratings(self, idx):
        # scores
        try:
            self.movie['user_score'] = float(self.page.select_one(
                'div#title-overview-widget strong > span').text)
        except:
            self.movie['user_score'] = None

        try:
            self.movie['user_count'] = int(self.page.select_one(
                'div#title-overview-widget div.imdbRating > a > span').text)
        except:
            self.movie['user_count'] = None

        # reviews
        reviews = self.page.select_one('div.hiddenImportant')
        if reviews is not None:
            reviews = reviews.text.split()
            if len(reviews) == 2:
                self.movie[reviews[1]] = int(reviews[0])
            else:
                self.movie[reviews[1]] = int(reviews[0])
                self.movie[reviews[3]] = int(reviews[2])
        self.db.insert_ratings(idx, self.movie)

    def summary(self, idx):
        self.movie['summary'] = self.page.select_one(
            'ul#plot-summaries-content li:nth-of-type(1) > p').text
        if re.match('It looks like we don\'t have any Plot Summaries', self.movie['summary']):
            self.movie['summary'] = None

        self.db.insert_summaries(idx, self.movie.get('summary'))

    def movie_people(self, idx):
        directors = self.page.select(
            'table:nth-of-type(1) > tbody > tr > td > a')
        writers = self.page.select(
            'table:nth-of-type(2) > tbody > tr > td > a')
        actors = self.page.select(
            'table.cast_list > tr > td:nth-of-type(2) > a')

        if directors is not []:
            for director in directors:
                self.credits.append({'role': 'director', 'person_id': int(director.get(
                    'href').split('/name/nm')[1][:-1]), 'name': director.text.strip()})

        if writers is not []:
            for writer in writers:
                self.credits.append({'role': 'writer', 'person_id': int(writer.get(
                    'href').split('/name/nm')[1][:-1]), 'name': writer.text.strip()})

        if actors is not []:
            for actor in actors:
                self.credits.append({'role': 'actor', 'person_id': int(
                    actor.get('href').split('/name/nm')[1][:-1]), 'name': actor.text.strip()})
        return self.credits


    def people(self, pidx):
        try:
            self.person['image'] = self.page.select_one(
                'div.image > a > img#name-poster').get('src')
        except:
            pass
        try:
            self.person['birthday'] = self.page.select_one(
                'div#name-born-info > time').text.strip()
        except:
            pass
        try:
            self.person['hometown'] = self.page.select_one(
                'div#name-born-info > a').text.strip()
        except:
            pass
        try:
            self.person['actor'] = int(self.page.select_one(
                'div#filmo-head-actor > a').findParent().text.split('(')[1].split()[0])
        except:
            pass
        try:
            self.person['actress'] = int(self.page.select_one(
                'div#filmo-head-actress > a').findParent().text.split('(')[1].split()[0])
        except:
            pass
        try:
            self.person['director'] = int(self.page.select_one(
                'div#filmo-head-director > a').findParent().text.split('(')[1].split()[0])
        except:
            pass
        try:
            self.person['writer'] = int(self.page.select_one(
                'div#filmo-head-writer > a').findParent().text.split('(')[1].split()[0])
        except:
            pass
        if self.person.get('actor') is not None:
            self.person['acting'] = int(self.person.get('actor'))
        elif self.person.get('actress') is not None:
            self.person['acting'] = int(self.person.get('actress'))
        else:
            pass

        self.db.insert_people(pidx, self.person)

    def movie_credits_commit(self, idx, credits):
        self.db.insert_credits(idx, credits)

    def commit(self):
        self.db.conn.commit()


if __name__ == '__main__':
    sql = db.DataBase('data')
    sql.cursor.execute('SELECT id FROM Movies')
    data = sql.cursor.fetchall()[:5]

    for idx in data:
        scrapper = Scrapper('https://www.imdb.com/title/tt000000{}/', idx[0])
        scrapper.details(idx[0])
        scrapper.companies(idx[0])
        scrapper.countries(idx[0])
        scrapper.genres(idx[0])
        scrapper.languages(idx[0])
        scrapper.ratings(idx[0])
        scrapper.commit()

        scrapper = Scrapper(
            'https://www.imdb.com/title/tt{}/plotsummary', idx[0])
        scrapper.summary(idx[0])
        scrapper.commit()

        scrapper = Scrapper(
            'https://www.imdb.com/title/tt{}/fullcredits', idx[0])
        for pidx in scrapper.movie_people(idx[0]):
            scrapper = Scrapper('https://www.imdb.com/name/nm{}/', pidx.get('person_id'))
            scrapper.people(pidx.get('person_id'))
            scrapper.movie_credits_commit(idx[0], pidx)
            scrapper.commit()
    sql.close_db()
    print('done')
