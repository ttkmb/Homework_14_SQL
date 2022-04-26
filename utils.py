import sqlite3
from flask import Flask, jsonify


def connect_to_db(query):
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        cur.execute(query)
        result = cur.fetchall()
    return result


def actors(actor1='Rose McIver', actor2='Ben Lamb'):
    query = f"""
            SELECT "cast"
            FROM netflix 
            WHERE "cast" LIKE "%{actor1}%"
            AND "cast" LIKE "%{actor2}%"
    """
    response = connect_to_db(query)
    actors = []
    for cast in response:
        actors.extend(cast[0].split(', '))
    result = []
    for name in actors:
        if name not in [actor1, actor2]:
            if actors.count(name) > 2:
                result.append(name)
    result = set(result)
    print(result)


def get_films(type_film='Movie', release_year=2016, genre='Dramas'):
    query = f"""
            SELECT title, description
            FROM netflix
            WHERE "type" = '{type_film}'
            AND listed_in LIKE '%{genre}%'
            AND release_year = {release_year}
    """
    response = connect_to_db(query)
    response_json = []
    for film in response:
        response_json.append({
            'title': film[0],
            'description': film[1]
        })
    return response_json
