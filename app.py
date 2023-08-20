from flask import (
   Flask, 
   render_template, 
   request, 
   abort, 
   jsonify)
from flask_cors import CORS
from sqlalchemy import exc
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth
import sys



def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, PUT, POST,DELETE, OPTIONS')
        return response
    

    @app.route('/')
    def index():
       return jsonify({'message':'welcome to casting agency :)'})
 

    """
    Movie APIs
 
    """

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()

        if len(movies) == 0:
          abort(404)

        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        }), 200
    

    @app.route("/movies/<int:movie_id>", methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        try:
          movie = Movie.query.get(movie_id)
          
          if movie is None:
             abort(404)

          movie.delete()
          
          return jsonify({
                'success': True,
                'deleted': movie_id,
                'message': 'Movie ('+ movie.title +') was successfully deleted'
            }), 200
        except:
            print(sys.exc_info())
            abort(422)
        
   
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
       body = request.get_json()
       title = body.get('title')
       release_date = body.get('release_date')
      

       if(title is None or release_date is None):
            abort(400)

       try:
         new_movie = Movie(title=title,
                           release_date=release_date
                           )
         
         new_movie.insert()
         
         return jsonify({
           "success": True,
           "created": new_movie.id,
           "total_movies": len(Movie.query.all()),
         })
       except:
         print(sys.exc_info())
         abort(422)

    @app.route('/movies/<int:movie_id>', methods=['GET', 'PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        body = request.get_json()
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie:
            movie.title = (body['title'] if body['title']
                           else movie.title)
            movie.release_date = (body['release_date'] if
                                  body['release_date'] else
                                  movie.release_date)
        else:
            abort(404)
        try:
            movie.update()

            return jsonify({
                'success': True,
                'movie': [movie.format()]
                }), 200
        except:
            print(sys.exc_info())
            abort(500)


    """
    Actor APIs
 
    """

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()

        if len(actors) == 0:
          abort(404)

        return jsonify({
            'success': True,
            'acorts': [actor.format() for actor in actors]
        }), 200
    

    @app.route("/actors/<int:actor_id>", methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        try:
          actor = Actor.query.get(actor_id)
          
          if actor is None:
             abort(404)

          actor.delete()
          
          return jsonify({
                'success': True,
                'deleted': actor_id,
                'message': 'Actor ('+ actor.name +') was successfully deleted'
            }), 200
        except:
            print(sys.exc_info())
            abort(422)
        
   
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
       body = request.get_json()
       name = body.get('name')
       age = body.get('age')
       gender = body.get('gender')
       movie_id = body.get('movie_id')
      

       if(name is None or age is None or gender is None or movie_id is None):
            abort(400)

       movie = Movie.query.get(movie_id)
          
       if movie is None:
           abort(404)

       try:
         new_actor = Actor(name= name, 
                           age= age,
                           gender= gender,
                           movie_id = movie_id
                           )
         
         new_actor.insert()
         
         return jsonify({
           "success": True,
           "created": new_actor.id,
           "total_actors": len(Actor.query.all()),
         })
       except:
         print(sys.exc_info())
         abort(422)

    @app.route('/actors/<int:actor_id>', methods=['GET', 'PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload,actor_id):
        body = request.get_json()
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor:
            actor.name = (body['name'] if body['name']
                           else actor.name)
            actor.age = (body['age'] if body['age'] 
                         else actor.age)
            actor.gender = (body['gender'] if body['gender'] 
                         else actor.gender)
            actor.movie_id = (body['movie_id'] if body['movie_id']
                              else actor.movie_id)          
        else:
            abort(404)

        movie = Movie.query.get( actor.movie_id )
        if movie is None:
           abort(404)

        try:
            actor.update()

            return jsonify({
                'success': True,
                'movie': [actor.format()]
                }), 200
        except:
            print(sys.exc_info())
            abort(500)



    @app.errorhandler(AuthError)
    def auth_error(error):
     return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


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
        "message": 'Bad Request'
    }), 400

    @app.errorhandler(401)
    def unauthorized(error):
     return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401

    @app.errorhandler(405)
    def method_not_allowed(error):
     return jsonify({
        "success": False,
        "error": 405,
        "message": 'Method Not Allowed'
    }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
     return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error'
    }), 500



    return app

app = create_app()


if __name__ == '__main__':
    app.run()