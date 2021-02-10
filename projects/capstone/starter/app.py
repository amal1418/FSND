import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from flask_migrate import Migrate


from models import setup_db, Actor, Movie

ELEMENTS_PER_PAGE = 20

def paginate_elements(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ELEMENTS_PER_PAGE
    end = start + ELEMENTS_PER_PAGE

    elements = [element.format() for element in selection]
    current_elements = elements[start:end]

    return current_elements

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    Get Actor and Movie 
    '''
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(jwt):

        actors = Actor.query.all()
        
        if not actors:
          abort(404)

        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        }), 200

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(jwt):

        movies = Movie.query.all()

        if not movies:
          abort(404)

        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        }), 200

    '''
    Get Actor and Movie by id
    '''
    @app.route('/actors/<int:actor_id>')
    @requires_auth('get:actors')
    def get_actors_by_id(jwt, actor_id):

      actor = Actor.query.get(actor_id)

      if not actor:
          abort(404)

      return jsonify({
            'success': True,
            'actors': actor.format()
      }), 200

    @app.route('/movies/<int:movie_id>')
    @requires_auth('get:movies')
    def get_movies_by_id(jwt, movie_id):

      movie = Movie.query.get(movie_id)

      if not movie:
          abort(404)

      return jsonify({
            'success': True,
            'movies': movie.format()
      }), 200

    '''
    Post Actor and Movie 
    '''
    @app.route('/actors', methods=['post'])
    @requires_auth('post:actors')
    def create_actor(jwt):
        try:
            body = request.get_json()

            name = body['name']
            age = body['age']
            gender = body['gender']

            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()

            return jsonify({
                'success': True,
                'created': actor.format()
            }), 200
        except Exception:
            abort(422)

    @app.route('/movies', methods=['post'])
    @requires_auth('post:movies')
    def create_movie(jwt):
        try:
            body = request.get_json()

            title = body['title']
            release_date = body['release_date']

            movie = Movie(title=title, release_date=release_date)
            movie.insert()

            return jsonify({
                'success': True,
                'created': movie.format()
            }), 200
        except Exception:
            abort(422)

    '''
    Patch Actor and Movie 
    '''
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor(jwt, actor_id):
      try:
        body = request.get_json()
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        
        if actor is None:
            abort(404)

        actor.name = body.get('name') or actor.name 
        actor.age = body.get('age') or actor.name 
        actor.gender = body.get('gender') or actor.gender
       
        actor.update()

        return jsonify({
            'success': True,
            'actors': actor.format()
        }), 200

      except Exception:
        abort(400)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(jwt, movie_id):
      try:
        body = request.get_json()
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        movie.title = body.get('title') or movie.title 
        movie.release_date = body.get('release_date') or movie.release_date 
       
        movie.update()

        return jsonify({
            'success': True,
            'movies': movie.format()
        }), 200

      except Exception:
        abort(400)

    '''
    Delete Actor and Movie 
    '''
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

      if actor is None:
        abort(404)

      actor.delete()

      return jsonify({
        'success': True,
        'deleted': actor_id
      }), 200

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

      if movie is None:
        abort(404)

      movie.delete()

      return jsonify({
        'success': True,
        'deleted': movie_id
      }), 200 

    '''
    Error handling for 422, 404 and Auth Error 
    '''
    @app.errorhandler(422)
    def unprocessable(error):
      return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
      }), 422

    @app.errorhandler(404)
    def not_found(error):
      return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
      }), 404

    @app.errorhandler(400)
    def bad_request(error):
      return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
      }), 400

    @app.errorhandler(AuthError)
    def auth_errorhandler(error):
      return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
      }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
