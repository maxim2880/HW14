import sqlite3
from collections import Counter


class DbConnect:
    def __init__(self, path):
        self.con = sqlite3.connect("netflix.db")
        self.cur = self.con.cursor()

    def __del__(self):
        self.cur.close()
        self.con.close()


def execute_query(query):
    """Функция создания запроса к базе, взамен класса"""
    with sqlite3.connect('netflix.db') as con:
        cur = con.cursor()
        cur.execute(query)
        result = cur.fetchall()
    return result


def movie_by_title(title):
    """Вывод информации по конкретному фильму"""
    db_connect = DbConnect("netflix.db")
    db_connect.cur.execute(
        f"""SELECT title, country, release_year, listed_in,
     description from netflix 
     where title like '%{title}%'
    order by release_year desc
    limit 1""")
    result = db_connect.cur.fetchone()
    return {
        "title": result[0],
        "country": result[1],
        "release_year": result[2],
        "genre": result[3],
        "description": result[4]
    }


def movies_by_years(year1, year2):
    """Вывод фильмов в диапазоне годов"""
    db_connect = DbConnect("netflix.db")
    query = f"select title, release_year from netflix where release_year between {year1} and {year2} limit 100"
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
                            "release_year": movie[1]})
    return result_list


def movies_by_rating(rating):
    """Вывод фильмов по определенному рейтингу"""
    rating_parameters = {
        "children": "'G'",
        "family": "'G', 'PG', 'PG-13'",
        "adult": "'R', 'NC-17'"
    }
    if rating not in rating_parameters:
        return "Некорректный рейтинг"
    db_connect = DbConnect("netflix.db")
    query = f"select title, rating, description from netflix where rating in ({rating_parameters[rating]})"
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({
            "title": movie[0],
            "rating": movie[1],
            "description": movie[2]
        })
    return result_list


def movies_by_genre(genre):
    """Вывод 10 свежих фильмов по жанру"""
    query = f"select title, description " \
            f"from netflix " \
            f"where listed_in like '%{genre}%' " \
            f"order by release_year desc limit 10"
    result = execute_query(query)
    result_list = []
    for movie in result:
        result_list.append({
            "title": movie[0],
            "description": movie[1]
        })
    return result_list


def cast_partners(actor1, actor2):
    """Возворащает список актеров, которые играли в паре больше 2 раз"""
    query = f"select `cast` from netflix " \
            f"where `cast` like '%{actor1}%' " \
            f"and `cast` like '%{actor2}%'"
    result = execute_query(query)
    actors_list = []
    for cast in result:
        actors_list.extend(cast[0].split(', '))
    counter = Counter(actors_list)
    result_list = []
    for actor, count in counter.items():
        if actor not in [actor1, actor2] and count > 2:
            result_list.append(actor)
    return result_list


def search_movie_by_param(movie_type, released_year, genre):
    """Поиск фильмов по ряду параметров"""
    query = f"select title, description " \
            f"from netflix where type = '{movie_type}' " \
            f"and release_year = {released_year} " \
            f"and listed_in like '%{genre}%'"
    result = execute_query(query)
    result_list = []
    for movie in result:
        result_list.append({
            'title': movie[0],
            'description': movie[1]})
    return result_list

print(search_movie_by_param('TV Show', 2005, 'Drama'))