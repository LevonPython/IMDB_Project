import sqlite3
import modify as mod
# import info


class DataBase:

    def __init__(self, file_name):
        self.conn = sqlite3.connect(f'{file_name}.db')
        self.conn.execute('PRAGMA foreign_keys = ON')
        self.cursor = self.conn.cursor()

    def create_table(self):
        try:
            self.conn.execute('''
                    CREATE TABLE IF NOT EXISTS Movies (
                        id INTEGER PRIMARY KEY,
                        title TEXT
                        )
                    ''')

            self.conn.execute('''
                    CREATE TABLE IF NOT EXISTS People (
                        id INTEGER PRIMARY KEY,
                        birthday DATETIME,
                        image TEXT,
                        hometown TEXT,
                        acting INTEGER,
                        director INTEGER,
                        writer INTEGER
                        )
                    ''')

            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS movie_people (
                        movie_id INTEGER,
                        person_id INTEGER,
                        name TEXT,
                        role TEXT,
                        FOREIGN KEY (movie_id) REFERENCES Movies (id)
                        FOREIGN KEY (person_id) REFERENCES People (id)
                        )
                    ''')

            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS movie_details (
                        movie_id INTEGER,
                        release_date DATETIME,
                        also_known_as TEXT,
                        budget TEXT,
                        opening_weekend_usa TEXT,
                        gross_usa TEXT,
                        cumulative_worldwide_gross TEXT,
                        runtime INTEGER,
                        color TEXT,
                        image TEXT,
                        FOREIGN KEY (movie_id) REFERENCES Movies (id)
                        )
                    ''')

            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS movie_ratings (
                        movie_id INTEGER,
                        user_score REAL,
                        user_count INTEGER,
                        user_reviews INTEGER,
                        critic_reviews INTEGER,
                        FOREIGN KEY (movie_id) REFERENCES Movies (id)
                        )
                    ''')

            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS movie_companies (
                        movie_id INTEGER,
                        company TEXT,
                        FOREIGN KEY (movie_id) REFERENCES Movies (id)
                        )
                    ''')

            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS movie_countries (
                        movie_id INTEGER,
                        country TEXT,
                        FOREIGN KEY (movie_id) REFERENCES Movies (id)
                        )
                    ''')

            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS movie_genres (
                        movie_id INTEGER,
                        genre TEXT,
                        FOREIGN KEY (movie_id) REFERENCES Movies (id)
                        )
                    ''')

            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS movie_languages (
                        movie_id INTEGER,
                        language TEXT,
                        FOREIGN KEY (movie_id) REFERENCES Movies (id)
                        )
                    ''')

            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS movie_summaries (
                        movie_id INTEGER,
                        summary TEXT,
                        FOREIGN KEY (movie_id) REFERENCES Movies (id)
                        )
                    ''')

            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS movie_oscars (
                        movie_id INTEGER,
                        title TEXT,
                        award TEXT,
                        year INTEGER,
                        result TEXT,
                        FOREIGN KEY (movie_id) REFERENCES Movies (id)
                        )
                    ''')

            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS people_oscars (
                        person_id INTEGER,
                        name TEXT,
                        award TEXT,
                        year INTEGER,
                        result TEXT,
                        FOREIGN KEY (person_id) REFERENCES People (id)
                        )
                    ''')

        except sqlite3.DatabaseError:
            self.conn.rollback()

    def insert_mids(self, idx, title):
        return self.cursor.execute("""INSERT into Movies (id,
                                            title)
                                VALUES (?,?)""",
                                   (int(idx),
                                    title
                                    ))

    def insert_details(self, idx, movie):
        print('------------------')
        return self.cursor.execute("""INSERT into movie_details (movie_id,
                                                    release_date,
                                                    also_known_as,
                                                    budget,
                                                    opening_weekend_usa,
                                                    gross_usa,
                                                    cumulative_worldwide_gross,
                                                    runtime,
                                                    color,
                                                    image)
                                    VALUES (?,?,?,?,?,?,?,?,?,?)""",
                                   (int(idx),
                                    mod.date_time(movie.get('release_date')),
                                       movie.get('also_known_as'),
                                       movie.get('budget'),
                                       movie.get('opening_weekend_usa'),
                                       movie.get('gross_usa'),
                                       movie.get('cumulative_worldwide_gross'),
                                       movie.get('runtime'),
                                       movie.get('color'),
                                       movie.get('image')
                                    ))

    def insert_companies(self, idx, company):
        return self.cursor.execute("""INSERT into movie_companies (movie_id,
                                                               company)
                                    VALUES (?,?)""",
                                   (int(idx),
                                    company
                                    ))

    def insert_countries(self, idx, country):
        return self.cursor.execute("""INSERT into movie_countries (movie_id,
                                                       country)
                            VALUES (?,?)""",
                                   (int(idx),
                                    country
                                    ))

    def insert_genres(self, idx, genre):
        return self.cursor.execute("""INSERT into movie_genres (movie_id,
                                                       genre)
                            VALUES (?,?)""",
                                   (int(idx),
                                    genre
                                    ))

    def insert_languages(self, idx, language):
        return self.cursor.execute("""INSERT into movie_languages (movie_id,
                                                       language)
                            VALUES (?,?)""",
                                   (int(idx),
                                    language
                                    ))

    def insert_ratings(self, idx, rating):
        return self.cursor.execute("""INSERT INTO movie_ratings (movie_id,
                                                    user_score,
                                                    user_count,
                                                    user_reviews,
                                                    critic_reviews)
                                    VALUES(?, ?, ?, ?, ?)""",
                                   (int(idx), rating.get('user_score'),
                                       rating.get('user_count'),
                                       rating.get('user'),
                                       rating.get('critic')
                                    ))

    def insert_summaries(self, idx, summary):
        return self.cursor.execute("""INSERT into movie_summaries (movie_id,
                                                                summary)
                            VALUES (?,?)""",
                                   (int(idx),
                                    summary
                                    ))

    def insert_people(self, idx, person):
        return self.cursor.execute("""INSERT or IGNORE into People (id,
                                                                   image,
                                                                   birthday,
                                                                   hometown,
                                                                   acting,
                                                                   director,
                                                                   writer)
                                    VALUES(?,?,?,?,?,?,?)""",
                                   (int(idx),
                                    person.get('image'),
                                    person.get('birthday'),
                                    person.get('hometown'),
                                    person.get('acting'),
                                    person.get('director'),
                                    person.get('writer')
                                    ))

    def insert_credits(self, idx, credit):
        return self.cursor.execute("""INSERT into movie_people (movie_id,
                                                        person_id,
                                                        name,
                                                        role)

                            VALUES (?,?,?,?)""",
                                   (int(idx),
                                    credit.get('person_id'),
                                    credit.get('name'),
                                    credit.get('role')
                                    ))

    def insert_movie_oscars(self, awards, result):
        print(awards.get('title'),
              awards.get('award'),
              awards.get('year'),
              result)
        return self.cursor.execute("""INSERT into movie_oscars (movie_id,
                                                        title,
                                                        award,
                                                        year,
                                                        result)

                            VALUES (?,?,?,?,?)""",
                                   (awards.get('movie_id'),
                                    awards.get('title'),
                                    awards.get('award'),
                                    awards.get('year'),
                                    result
                                    ))

    def insert_credit_oscars(self, awards, result):
        print(int(awards.get('person_id')),
              awards.get('name'),
              awards.get('award'),
              awards.get('year'))
        return self.cursor.execute("""INSERT into people_oscars (person_id,
                                                        name,
                                                        award,
                                                        year,
                                                        result)

                            VALUES (?,?,?,?,?)""",
                                   (int(awards.get('person_id')),
                                    awards.get('name'),
                                    awards.get('award'),
                                    awards.get('year'),
                                    result
                                    ))

    def close_db(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    db = DataBase('data')
    db.create_table()
    db.close_db()
    print('closed')
