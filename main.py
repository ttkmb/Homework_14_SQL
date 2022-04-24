import sqlite3
from flask import Flask, jsonify


def main():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False

    def connect_to_db(query):
        with sqlite3.connect("netflix.db") as con:
            cur = con.cursor()
            cur.execute(query)
            result = cur.fetchall()
        return result

    @app.route("/movie/<title>")
    def get_movie_by_title(title):
        query = f"""
                SELECT title, country, release_year, listed_in as genre, description
                FROM netflix
                WHERE title = '{title}'
                ORDER BY release_year DESC
                LIMIT 1
        """
        response = connect_to_db(query)[0]
        response_json = {
            'title': response[0],
            'country': response[1],
            'release_year': response[2],
            'genre': response[3],
            'description': response[4]
        }
        return jsonify(response_json)

    @app.route("/movie/<int:year>/to/<int:year2>")
    def get_movies_by_year(year, year2):
        query = f"""
               SELECT title, release_year
               FROM netflix
               WHERE release_year BETWEEN {year} AND {year2} 
               ORDER BY release_year 
               LIMIT 100
        """
        response = connect_to_db(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'release_year': film[1]
            })
        return jsonify(response_json)

    @app.route("/rating/<group>")
    def get_movie_for_group(group):
        groups = {
            'children': ['G'],
            'family': ['G', 'PG', 'PG-13'],
            'adult': ['R', 'NC-17']
        }
        if group in groups:
            level = '\", \"'.join(groups[group])
            level = f'\"{level}\"'
        else:
            return jsonify([])
        query = f"""
                    SELECT title, rating, description
                    FROM netflix
                    WHERE rating IN ({level})
            """
        response = connect_to_db(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'rating': film[1],
                'description': film[2]
            })
        return jsonify(response_json)

    @app.route("/genre/<genre>")
    def get_movie_by_genre(genre):
        query = f"""
                        SELECT title, description 
                        FROM netflix
                        WHERE listed_in LIKE '%{genre}%'
                        ORDER BY release_year desc
                        LIMIT 10
                """
        response = connect_to_db(query)
        response_json = []
        for film in response:
            response_json.append({
                'title': film[0],
                'description': film[1]
            })
        return jsonify(response_json)

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

    # actors()
    # app.run(debug=True)

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
        return (response_json)

    print(get_films())


if __name__ == '__main__':
    main()
