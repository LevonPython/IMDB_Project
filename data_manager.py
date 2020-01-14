import sqlite3
import os
from datetime import datetime


class MovieManager:

    def __init__(self):
        path = f"{os.getcwd().replace('application', 'data')}\data.db"
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.number_page = 10
        self.page_size = 30

    def movie_page(self, page, query):
        sql = """SELECT movies.id, movies.title, movie_summaries.summary,
                     movie_details.image, movie_ratings.user_reviews
                     FROM movies
                    Left JOIN movie_ratings ON movie_ratings.movie_id=movies.id
                    Left JOIN movie_details ON movie_details.movie_id=movies.id
                    Left JOIN movie_summaries ON
                    movie_summaries.movie_id=movies.id
                    WHERE UPPER(title) LIKE :query OR
                    UPPER(summary) LIKE :query
                    ORDER BY user_reviews DESC
                    LIMIT {}, {}""".format((page - 1) * self.page_size,
                                           self.page_size)

        self.cur.execute(sql, {'query': f'%{query}%'})

        return self.cur.fetchall()

    def movie_count(self, query):
        sql = """SELECT movies.id, movie_summaries.summary,
                 movie_ratings.user_reviews, COUNT(*) max_count FROM movies
                 Left JOIN movie_ratings ON movie_ratings.movie_id=movies.id
                 Left JOIN movie_summaries ON
                 movie_summaries.movie_id=movies.id
                 WHERE UPPER(title) LIKE :query OR UPPER(summary) LIKE :query
                 ORDER BY user_reviews DESC"""

        self.cur.execute(sql, {'query': f'%{query}%'})

        return self.cur.fetchone()['max_count']

    def celebs(self, page, query):
        sql = """SELECT * FROM people
                WHERE image is not Null
                AND UPPER(name) LIKE :query Order by rating DESC
                LIMIT {}, {} """

        self.cur.execute(sql.format((page - 1) * self.page_size,
                                    self.page_size), {'query': f'%{query}%'})
        return self.cur.fetchall()

    def celebs_count(self, query):
        sql = """SELECT *, COUNT(DISTINCT people.id) max_count FROM people
                WHERE image is not Null
                AND UPPER(name) LIKE :query"""
        self.cur.execute(sql, {'query': f'%{query}%'})

        return self.cur.fetchone()['max_count']

    def ordered_data(self, feature, page, query):
        sql = f"""SELECT * FROM Movies
                INNER JOIN movie_ratings ON movie_ratings.movie_id=Movies.id
                INNER JOIN movie_details ON movie_details.movie_id=Movies.id
                INNER JOIN movie_summaries ON
                movie_summaries.movie_id=Movies.id
                WHERE UPPER(title) LIKE :query OR UPPER(summary) LIKE :query
                ORDER BY {feature} DESC
                LIMIT {(page - 1) * self.page_size}, {self.page_size}"""

        self.cur.execute(sql, {'query': f'%{query}%'})

        return self.cur

    def ordered_data_count(self, feature, query):
        sql = f"""SELECT *, COUNT(*) max_count FROM Movies
                INNER JOIN movie_ratings ON movie_ratings.movie_id=Movies.id
                INNER JOIN movie_details ON movie_details.movie_id=Movies.id
                INNER JOIN movie_summaries ON
                movie_summaries.movie_id=Movies.id
                WHERE UPPER(title) LIKE :query OR UPPER(summary) LIKE :query
                ORDER BY {feature} DESC"""

        self.cur.execute(sql, {'query': f'%{query}%'})
        return self.cur.fetchone()['max_count']

    def genres_page(self, genre, page):
        sql = """SELECT * FROM movie_genres
                INNER JOIN Movies ON movie_genres.movie_id=Movies.id
                INNER JOIN movie_ratings ON movie_ratings.movie_id=Movies.id
                INNER JOIN movie_details ON movie_details.movie_id=Movies.id
                INNER JOIN movie_summaries ON
                movie_summaries.movie_id=Movies.id
                WHERE movie_genres.genre=(?)
                ORDER BY user_reviews DESC
                LIMIT {}, {}"""

        self.cur.execute(sql.format((page - 1) * self.page_size,
                                    self.page_size), (genre,))
        return self.cur

    def genre_count(self, genre):
        sql = """SELECT *, COUNT(*) max_count FROM movie_genres
                INNER JOIN Movies ON movie_genres.movie_id=Movies.id
                INNER JOIN movie_ratings ON movie_ratings.movie_id=Movies.id
                INNER JOIN movie_details ON movie_details.movie_id=Movies.id
                INNER JOIN movie_summaries ON
                movie_summaries.movie_id=Movies.id
                WHERE movie_genres.genre=(?)
                ORDER BY user_reviews DESC
                """
        self.cur.execute(sql, (genre,))

        return self.cur.fetchone()['max_count']

    def oscars(self):
        query_movie = """SELECT movie_oscars.movie_id, movie_oscars.title,
                         movie_oscars.award, UPPER(movie_oscars.result) result,
                         movie_details.image, movie_oscars.year
                         From movie_oscars LEFT JOIN movie_details ON
                         movie_oscars.movie_id = movie_details.movie_id
                         ORDER BY movie_oscars.year DESC,
                         movie_oscars.award DESC, movie_oscars.result DESC"""

        query_person = """SELECT people_oscars.person_id, People.name,
                          people_oscars.award, UPPER(people_oscars.result)
                          result, People.image, people_oscars.year
                          FROM people_oscars LEFT JOIN People ON
                          people_oscars.person_id = People.id
                          ORDER BY people_oscars.year DESC,
                          people_oscars.award DESC, people_oscars.result
                          DESC"""

        query = {'query_movie': query_movie, 'query_person': query_person}

        data = {query_name: self.cur.execute(query[query_name]).fetchall()
                for query_name in query}
        # grouping by years and awards
        years = list({movie['year'] for movie in data['query_movie']})
        award = {}
        for year in years[::-1]:
            award[year] = set()
            for movie in data['query_movie']:
                if movie['year'] == year:
                    award[year].add(movie['award'])
            for person in data['query_person']:
                if person['year'] == year:
                    award[year].add(person['award'])
            award[year] = list(award[year])
            award[year].sort()
        return {'award': award, 'data': data}

    def person_data(self, id):
        sql_people = """Select DISTINCT *  From people
                        Where people.id = (?)"""
        sql_oscar = """Select * From  people_oscars where person_id = (?)"""
        sql_movies = """ Select DISTINCT movie_people.movie_id,
                         movies.title,
                         movie_details.also_known_as, movie_details.image,
                         movie_details.date_year, movie_summaries.summary
                         FROM movie_people Left Join movies
                         ON movie_people.movie_id = movies.id
                         Left Join movie_details ON
                         movie_people.movie_id = movie_details.movie_id
                         Left Join movie_summaries ON
                         movie_people.movie_id = movie_summaries.movie_id
                         Where person_id = (?)"""
        query = {'person': sql_people, 'oscar': sql_oscar,
                 'movies': sql_movies}
        data = {query_: self.cur.execute(query[query_], (id,)).fetchall()
                for query_ in query}
        # --- changing birthday date format --- #
        for person in data['person']:
            if person['birthday'] is not None:
                data['birthday'] = (datetime.strptime(person['birthday'],
                                    '%Y-%m-%d')).strftime('%Y-%b-%d')
            else:
                data['birthday'] = '---'
        return data

    def movie_sep_data(self, id):
        sql_genres = """SELECT genre FROM movie_genres WHERE movie_id=(?)"""
        cast = """SELECT Distinct people.id, people.image,
                  people.name FROM people Left JOIN
                  movie_people ON movie_people.person_id=people.id
                  WHERE movie_id=(?) and role = 'actor'
                  Limit 30"""
        other = """Select Distinct movie_people.role, people.name
                    From people Left Join movie_people 
                    On movie_people.person_id=people.id
                    WHERE movie_id=(?) and role != 'actor'"""
        sql_movie = """SELECT movies.id, movies.title,movie_details.color, 
                       movie_details.release_date, movie_details.runtime,
                       movie_details.budget, movie_details.gross_usa,
                       movie_details.cumulative_worldwide_gross,
                       movie_details.image, movie_summaries.summary,
                       movie_ratings.user_score, movie_ratings.user_count
                       FROM movies Left JOIN movie_ratings ON
                       movie_ratings.movie_id = movies.id Left JOIN
                       movie_details ON movie_details.movie_id = movies.id
                       Left JOIN movie_summaries ON
                       movie_summaries.movie_id = movies.id
                       WHERE movies.id=(?)"""
        sql_language = """ select language from movie_languages
                           where movie_id = (?)"""
        sql_country = """ select country from movie_countries
                          where movie_id = (?)"""
        sql_company = """ select company from movie_companies
                          where movie_id = (?)"""
        sql_oscar = """ select award, year, result from movie_oscars
                        where movie_id = (?)"""
        query = {'sql_genres': sql_genres, 'cast': cast, 'other': other, 'sql_movie': sql_movie,
                 'sql_language': sql_language, 'sql_country': sql_country,
                 'sql_company': sql_company, 'sql_oscar': sql_oscar}

        result = {query_: self.cur.execute(query[query_], [id, ]).fetchall()
                  for query_ in query}

        # changing format of data
        languages = ',   '.join(sorted({i[0] for i in result['sql_language']}))
        countries = ',   '.join(sorted({i[0] for i in result['sql_country']}))
        genres = ',   '.join(sorted({i[0] for i in result['sql_genres']}))

        result['sql_language'] = languages
        result['sql_country'] = countries
        result['sql_genres'] = genres
        company_set = set()
        for i in result['sql_company']:
            if i[0] is not None:
                company_set.add(i[0])
        if len(company_set) >= 1:
            companies = ',  '.join(company_set)
        else:
            companies = "---"
        result['sql_company'] = companies
        return result

