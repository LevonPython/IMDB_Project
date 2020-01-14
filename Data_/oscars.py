from selenium import webdriver
import init_sql as db
import time


class Scrapper:
    def __init__(self):
        self.base_url = 'https://www.imdb.com/event/ev0000003/{}/1/'
        self.list_movie_awards = ['Best Motion Picture of the Year',
                                  'Best Picture',
                                  'Best Animated Feature Film',
                                  'Best Adapted Screenplay',
                                  'Best Achievement in Cinematography',
                                  'Best Cinematography',
                                  'Best Achievement in Film Editing',
                                  'Best Film Editing',
                                  'Best Achievement in Production Design',
                                  'Best Achievement in Costume Design',
                                  'Best Achievement in Visual Effects',
                                  'Best Documentary Feature',
                                  'Best Documentary Short Subject',
                                  'Best Animated Feature Film']
        self.list_people_awards = ['Best Performance by an Actor in a Leading Role',
                                   'Best Actor in a Leading Role',
                                   'Best Performance by an Actress in a Leading Role',
                                   'Best Actress in a Leading Role',
                                   'Best Performance by an Actor in a Supporting Role',
                                   'Best Actor in a Supporting Role',
                                   'Best Performance by an Actress in a Supporting Role',
                                   'Best Actress in a Supporting Role',
                                   'Best Achievement in Directing',
                                   'Best Director']
        self.movie_awards_idx = []
        self.movie_winners = []
        self.movie_nominees = []
        self.credit_awards_idx = []
        self.credit_winners = []
        self.credit_nominees = []
        self.db = db.DataBase('oscars')
        self.db.create_table()
        self.browser = webdriver.Chrome()

    def oscars(self, year):

        time.sleep(2)
        self.browser.get(self.base_url.format(year))
        time.sleep(4)

        # getting the list of objects
        awards = [award.text for award in self.browser.find_elements_by_css_selector(
            'div#center-3-react div > div.event-widgets__award-category-name')]

        for i in awards:
            if i in self.list_movie_awards:
                self.movie_awards_idx.append(awards.index(i) + 1)

        for i in awards:
            if i in self.list_people_awards:
                self.credit_awards_idx.append(awards.index(i) + 1)

        for idx in self.movie_awards_idx:
            option_links = self.browser.find_elements_by_css_selector(f'div#center-3-react div:nth-child(1) > h3 > div:nth-child({idx}) > div.event-widgets__award-category-nominations > div > div > div.event-widgets__nomination-details > div.event-widgets__nominees > div.event-widgets__primary-nominees > span > span > a')

            self.movie_winners.append({'movie_id': option_links[0].get_attribute("href").split('tt')[2].split('/')[0],
                                       'title': option_links[0].text,
                                       'award': awards[idx - 1],
                                       'year': year})
            for link in option_links[1:]:
                self.movie_nominees.append({'movie_id': link.get_attribute("href").split('tt')[2].split('/')[0],
                                            'title': link.text,
                                            'award': awards[idx - 1],
                                            'year': year})

        for idx in self.credit_awards_idx:
            option_links = self.browser.find_elements_by_css_selector(f'div#center-3-react div:nth-child(1) > h3 > div:nth-child({idx}) > div.event-widgets__award-category-nominations > div > div > div.event-widgets__nomination-details > div.event-widgets__nominees > div.event-widgets__primary-nominees > span > span > a')

            self.credit_winners.append({'person_id': option_links[0].get_attribute("href").split('nm')[1].split('/')[0],
                                        'name': option_links[0].text,
                                        'award': awards[idx - 1],
                                        'year': year})
            for link in option_links[1:]:
                self.credit_nominees.append({'person_id': int(link.get_attribute("href").split('nm')[1].split('/')[0]),
                                             'name': link.text,
                                             'award': awards[idx - 1],
                                             'year': year})

        for movie_winner in self.movie_winners:
            try:
                sql.insert_movie_oscars(movie_winner, 'winner')
            except Exception as ex:
                print(ex)
                pass

        for movie_nominee in self.movie_nominees:
            try:
                sql.insert_movie_oscars(movie_nominee, 'nominee')
            except Exception as ex:
                print(ex)
                pass

        for credit_winner in self.credit_winners:
            try:
                sql.insert_credit_oscars(credit_winner, 'winner')
            except Exception as ex:
                print(ex)
                pass

        for credit_nominee in self.credit_nominees:
            try:
                sql.insert_credit_oscars(credit_nominee, 'nominee')
            except Exception as ex:
                print(ex)
                pass


if __name__ == '__main__':
    sql = db.DataBase('oscars')
    scrapper = Scrapper()
    for year in range(2010, 2012):
        print(year)
        scrapper.oscars(year)
        sql.conn.commit()
    scrapper.browser.close()
    sql.close_db()
    print('done')
