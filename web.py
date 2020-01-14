import math
from data_manager import MovieManager
from flask import Flask, render_template, request

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/movies')
def movies():
    # get paging parameter from GET string
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    # set detault to 1 if page is less than 1
    if page < 1:
        page = 1
    original_query = request.args.get('query', '')
    query = original_query.upper()
    movie_manager = MovieManager()
    max_count = movie_manager.movie_count(query)
    page_count = math.ceil(max_count / movie_manager.page_size)

    if page > page_count:
        page = page_count

    movies = movie_manager.movie_page(page, query)
    return render_template('movies.html', movies=movies, query=original_query,
                           page_count=page_count, page=page,
                           max_count=max_count,
                           number=movie_manager.number_page)


@app.route('/m_order_by/<feature>')
def order_by(feature):
    # get paging parameter from GET string
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    # set detault to 1 if page is less than 1
    if page < 1:
        page = 1

    original_query = request.args.get('query', '')
    query = original_query.upper()
    movie_manager = MovieManager()
    max_count = movie_manager.ordered_data_count(feature, query)
    page_count = math.ceil(max_count / movie_manager.page_size)

    if page > page_count:
        page = page_count
    cursor = movie_manager.ordered_data(feature, page, query)

    return render_template('movies.html', movies=cursor, query=original_query,
                           page_count=page_count, page=page,
                           max_count=max_count,
                           number=movie_manager.number_page)


@app.route('/movie/<idx>')
def movie(idx):
    movie_manager = MovieManager().movie_sep_data(idx)
    return render_template('movie_idx.html',
                           movies=movie_manager['sql_movie'],
                           genres=movie_manager['sql_genres'],
                           cast=movie_manager['cast'],
                           oscars=movie_manager['sql_oscar'],
                           languages=movie_manager['sql_language'],
                           country=movie_manager['sql_country'],
                           company=movie_manager['sql_company'],
                           other=movie_manager['other'])


@app.route('/celebs')
def celebs():
    # get paging parameter from GET string
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
    # set detault to 1 if page is less than 1
    if page < 1:
        page = 1
    original_query = request.args.get('query', '')
    query = original_query.upper()
    movie_manager = MovieManager()
    max_count = movie_manager.celebs_count(query)
    page_count = math.ceil(max_count / movie_manager.page_size)

    if page > page_count:
        page = page_count
    people = movie_manager.celebs(page, query)

    return render_template('celebs.html', people=people, query=original_query,
                           page_count=page_count, page=page,
                           max_count=max_count,
                           number=movie_manager.number_page)


@app.route('/name/<idx>')
def person(idx):
    movie_manager = MovieManager()
    persons = movie_manager.person_data(idx)['person']
    birthday = movie_manager.person_data(idx)['birthday']
    movies = movie_manager.person_data(idx)['movies']
    person_oscar = movie_manager.person_data(idx)['oscar']

    return render_template('person_idx.html', persons=persons,
                           birthday=birthday, movies=movies,
                           person_oscar=person_oscar)


@app.route('/genres/<genre>')
def genres(genre):
    query = ''
    # get paging parameter from GET string
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    # set detault to 1 if page is less than 1
    if page < 1:
        page = 1

    movie_manager = MovieManager()
    max_count = movie_manager.genre_count(genre)
    page_count = math.ceil(max_count / movie_manager.page_size)
    if page > page_count:
        page = page_count
    cursor = movie_manager.genres_page(genre, page)
    return render_template('genres.html', movies=cursor,
                           page_count=page_count, page=page,
                           max_count=max_count, genre=genre,
                           number=movie_manager.number_page, query=query)


@app.route('/oscars')
def oscars():
    movie_manager = MovieManager()
    result = movie_manager.oscars()['data']
    award = movie_manager.oscars()['award']
    return render_template('oscars.html', result=result, award=award)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run('127.0.0.1', 5055, True)
