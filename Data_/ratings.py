import sqlite3


class RatingCalculation:
    def __init__(self, id):
        self.id = id
        self.movie_value = 0
        with sqlite3.connect('data.db') as conn:
            self.cursor = conn.cursor()

    def movie_oscar(self):
        self.movie_value = 0
        sql = """ Select movie_people.movie_id, movie_people.person_id,
                  movie_oscars.result, movie_oscars.year, movie_oscars.award
                  From movie_people
                  Left Join movie_oscars On movie_oscars.movie_id = movie_people.movie_id
                  Where movie_people.person_id = (?)"""

        self.cursor.execute(sql, (self.id,))
        result = self.cursor.fetchall()
        for oscar in result:
            if oscar[2] == 'winner':
                self.movie_value += 0.1
            elif oscar[2] == 'nominee':
                self.movie_value += 0.05
            else:
                continue

        return self.movie_value

    def people_oscar(self):
        self.value = 0
        sql = """ Select * From people_oscars
                  Where person_id = (?)"""

        self.cursor.execute(sql, (self.id,))
        result = self.cursor.fetchall()
        for oscar in result:
            if oscar[3] == 'winner':
                self.value += 0.2
            elif oscar[3] == 'nominee':
                self.value += 0.1
            else:
                continue

        return self.value

    def votes(self):
        self.count = 0
        self.rating = 0
        sql = """ Select distinct movie_people.movie_id, movie_people.person_id,
                  movie_ratings.user_count, movie_ratings.user_score
                  From movie_people
                  Left Join movie_ratings On movie_ratings.movie_id = movie_people.movie_id
                  Where movie_people.person_id = (?) and  movie_ratings.user_count >= 20000"""

        self.cursor.execute(sql, (self.id,))
        result = self.cursor.fetchall()
        for vote in result:
            if vote[2] is None:
                continue
            self.count += 1
            self.rating += vote[3]
        if self.count == 0 or self.rating == 0:
            return 0
        return self.rating/self.count

    def calculation(self):
        movie_result = self.movie_oscar()
        rating = self.votes()
        person_result = self.people_oscar()
        final_rating = round(movie_result + rating + person_result, 2)
        if final_rating == 0:
            return "No info"
        return final_rating


if __name__ == "__main__":
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute("""SELECT DISTINCT id FROM people""")
    idx = cur.fetchall()
    for id in idx:
        rating = RatingCalculation(id).calculation()
        cur.execute("""UPDATE people SET rating = ? WHERE id = ?""", (rating, id))
    conn.commit()
    cur.close()
    conn.close()