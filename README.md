# Casting-Agency

"Casting Agency" is a web application that allows users with different roles to manage actors and movies in a database.

## Motivation

This project for `Udacity Full Stack web development nanondegree`.

The project covers the following concept 
- data modeling using `postgres`.
- API Architecture and Testing and testing using `Flask`.
- Authorization with RBAC and authentication using Third-Party Authentication auth0.
- API deployment using `render`.

## Project URLS

Render: https://render-deployment-casting-agency.onrender.com

Localhost: http://127.0.0.1:5000/

## Prerequisite
This project reuired:
- python 3: https://www.python.org/downloads/
- postgresql: https://www.postgresql.org/download/
- flask: https://pypi.org/project/Flask/

## Getting Started

### Running Locally
##### Create Your Virtual Environment
 To initialize and activate a virtualenv, run the following commands:
  - cd YOUR_PROJECT_DIRECTORY_PATH/
  - virtualenv --no-site-packages env
  - source env/bin/activate

##### Install Project Dependencies
To install project dependencies, run the following command:
 - pip install -r requirements.txt

##### Database Setup
To setup your local database:
 - create your database using 'createdb -U postgres casting_agency' command.
 - in 'models.py':
   - uncomment line 9-12 and update thoese lines with your user, host
   - comment line 13

##### Run Flask Server
To start running the project locally, run the following command - make sure yor virtual environment is active-:
 - export FLASK_APP=sample
 - export FLASK_ENV=development
 - flask run

## Authentication and authorization
 - how to setup your auth0: https://auth0.com/docs/applications
### Roles
In Auth0 Create three roles:

#### Casting Assistant
- Can view actors and movies.
#### Casting Director
- All permissions a Casting Assistant has.
- Add or delete an actor from the database.
- Modify actors or movies.
#### Executive Producer
- All permissions a Casting Director has.
- Add or delete a movie from the database.

### Permissions
Following permissions should be created under created API settings.

- `get:movies`
- `patch:movies`
- `post:movies`
- `delete:movies`
- `get:actors`
- `delete:actors`
- `post:actors`
- `patch:actors`

### Testing
To test the project:
- create your database using 'createdb -U postgres casting_agency_test' command.
- update the database url in 'test_app' [line 15].
- update the tokens in the class with valid tokens. use this link to get token (https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}})
- run the test using 'python test_app.py' command.


## API Reference

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Unprocessable 
- 405: Method not allowed
- 500: Internal Server Error

### Endpoints 
#### GET /movies
- General:
    - Returns a list of movies that contains id, release date, title  
    - Success value
- Sample: `curl -H "Authorization: Bearer <Token>" http://127.0.0.1:5000/movies`

``` {
"movies": [
    {
      "id": 5,
      "release_date": "Wed, 12 Jan 2022 00:00:00 GMT",
      "title": "Gintama"
    },
    {
      "id": 7,
      "release_date": "Sat, 07 Mar 2020 00:00:00 GMT",
      "title": "Gintama the movie"
    }
  ],
  "success": true
}
```
#### GET /actors
- General:
    - Returns a list of actors that contains id, age, gender, movie_id, name 
    - Success value
- Sample: `curl -H "Authorization: Bearer <Token>" http://127.0.0.1:5000/actors`

``` {
    "acorts": [
    {
      "age": 25,
      "gender": "male",
      "id": 4,
      "movie_id": 5,
      "name": "tom holland"
    },
    {
      "age": 58,
      "gender": "male",
      "id": 5,
      "movie_id": 5,
      "name": "Robert doney .jr"
    }
  ],
  "success": true
}
```
#### DELETE /movies/{movie_id}
- General:
    - Deletes the movie of the given ID if it exists. Returns the id of the deleted movie, success value, a confirmation message. 
- `curl -X DELETE http://127.0.0.1:5000/movies/5 -H "Authorization: Bearer <Token>"`
```
{
  "deleted": 5,
  "message": "Movie (Gintama) was successfully deleted",
  "success": true
}
```
#### DELETE /actors/{actor_id}
- General:
    - Deletes the actor of the given ID if it exists. Returns the id of the deleted actor, success value, a confirmation message. 
- `curl -X DELETE http://127.0.0.1:5000/actors/6 -H "Authorization: Bearer <Token>"`
```
{
  "deleted": 6,
  "message": "Actor (Robert doney .jr) was successfully deleted",
  "success": true
}
```
#### POST /movies
- General:
    - Creates a new movie using the submitted title, release date. Returns the id of the created movie, success value, total movies.
- `curl -X POST http://127.0.0.1:5000/movies -H "Content-Type: application/json" -H "Authorization: Bearer <Token>" -d '{"title" : "the batman", "release_date" : "04/03/2022"}'`
```
{
  "created": 9,
  "success": true,
  "total_movies": 3
}
```
#### POST /actors
- General:
    - Creates a new actor using the submitted name, age, gender, movie_id. Returns the id of the created actor, success value, total actors.
- `curl -X POST http://127.0.0.1:5000/actors -H "Content-Type: application/json" -H "Authorization: Bearer <Token>" -d '{"name" : "Robert Pattinson", "age" : "37", "gender":"male", "movie_id":"9"}'`
```
{
  "created": 7,
  "success": true,
  "total_actors": 1
}
```
#### PATCH /movies/{movie_id}
- General:
    - Update the movie of the given ID using the submitted title, release date. Returns the id, relase date, title, success value.
- `curl -X PATCH http://127.0.0.1:5000/movies/7 -H "Content-Type: application/json" -H "Authorization: Bearer <Token>" -d '{"title" : "the batman", "release_date" : "04/03/2022"}'`
```
{
  "movie": [
    {
      "id": 7,
      "release_date": "Sun, 03 Apr 2022 00:00:00 GMT",
      "title": "the batman"
    }
  ],
  "success": true
}
```
#### PATCH /actors/{avtor_id}
- General:
    - Update the actor of the given ID using the submitted name, age, gender, movie_id. Returns the id, relase date, title, success value.
- `curl -X PATCH http://127.0.0.1:5000/actors/7 -H "Content-Type: application/json" -H "Authorization: Bearer <Token>" -d '{"name" : "Robert", "age" : "", "gender" : "", "movie_id": ""}'`
```
{
  "movie": [
    {
      "age": 37,
      "gender": "male",
      "id": 7,
      "movie_id": 9,
      "name": "Robert"
    }
  ],
  "success": true
}
```
