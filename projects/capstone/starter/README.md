# Full Stack CAPSTONE project 
## Casting Agency 

This is the capstone project for the my Full Stack Development nanodegree, it models a company that is responsilbe for creating movies and manage the actors in this company and assign them to the movies.
The Authorized users can accesse this API to View, Add, Edit, Delete the movies and actors. 
## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running the server

first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

# API Reference

## Getting started

- Live URL: https://amal-casting-agency.herokuapp.com/ 

- Running Locally: the app is hosted by default in http://127.0.0.1:5000/ 


## Errors

When any error rises it will be returend as JSON object in this format: 

```
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```
There are three types of error when requests fail:

- 400: bad request 

- 404: resource not found 

- 422: unprocessable

## Endpoints
there are  endpoints in this API: 

1- GET/actors

2- GET/movies

3- GET/actors <actor_id>

4- GET/movies <movie_id>

5- POST/actors

6- POST/movies 

7- PATCH/actors 

8- PATCH/movies

9- DELETE/actors

10- DELETE/movies


### GET /actors

Genral: return list of the existed actors.
sample: curl http://127.0.0.1:5000/actors

```
{
    "actors": [
        {
            "age": 20,
            "gender": "male",
            "id": 1,
            "name": "Ahmad"
        },
        {
            "age": 21,
            "gender": "female",
            "id": 2,
            "name": "Maha"
        }
    ],
    "success": true
}

```

### GET /movies 

Genral: return list of the existed movies.
sample: curl http://127.0.0.1:5000/movies 

```
 {
    "movies": [
        {
            "id": 1,
            "release_date": "2020",
            "title": "the room"
        },
        {
            "id": 2,
            "release_date": "2021",
            "title": "The end"
        }
    ],
    "success": true
}
```

### GET /actors/<actor_id>
Genral: return a specific actor by ID.
sample: curl http://127.0.0.1:5000/actors/1

```
{
    "actors": {
        "age": 20,
        "gender": "male",
        "id": 1,
        "name": "Ahmad"
    },
    "success": true
}
```

### GET /movies/<movie_id>
Genral: return a specific movie by ID.
sample: curl http://127.0.0.1:5000/movies/1

```
{
    "movies": {
        "id": 2,
        "release_date": "2021",
        "title": "the end"
    },
    "success": true
}
```

### POST /actors

Genral: Post an actor with name, his age and gender.
it will returens the actor that created and the seccess value.
sample: curl -X POST http://127.0.0.1:5000/actors -H "Content-Type: application/json" -d '{"name":"Khalid", "age":"20", "gender":"female"}'

```
{
    "created": {
        "age": 20,
        "gender": "male",
        "id": 5,
        "name": "khalid"
    },
    "success": true
}

```

### POST /movies

Genral: Post a movie with title and the release date.
it will returens the movie that created and the seccess value.
sample: curl -X POST http://127.0.0.1:5000/movies -H "Content-Type: application/json" -d '{"title":"the night", "release_date":"2020"}'

```
{
    "created": {
        "id": 5,
        "release_date": "2020",
        "title": "the night"
    },
    "success": true
}

```

### PATCH /actors

Genral: edit the actor information.
it will returens the actor that edited and the seccess value.
sample: curl -X PATCH http://127.0.0.1:5000/actors -H "Content-Type: application/json" -d '{"age":"23"}'

```
{
    "actors": {
        "age": 23,
        "gender": "male",
        "id": 6,
        "name": "Ahmad"
    },
    "success": true
}

```

### PATCH /movies

Genral: edit the movie information.
it will returens the movie that edited and the seccess value.
sample: curl -X PATCH http://127.0.0.1:5000/movies -H "Content-Type: application/json" -d '{"title":"the room"}'

```
{
    "movies": {
        "id": 6,
        "release_date": "2020",
        "title": "the room"
    },
    "success": true
}

```


### DELETE /actors/<actor_id>

Genral: Delete an actor using actor ID and return the deleted actor ID with the seccess value .
sample: curl -X DELETE http://127.0.0.1:5000/actors/10

```
{
    "deleted": 10,
    "success": true
}

```

### DELETE /movies/<movie_id>

Genral: Delete an movie using movie ID and return the deleted movie ID with the seccess value .
sample: curl -X DELETE http://127.0.0.1:5000/movies/10

```
{
    "deleted": 10,
    "success": true
}

```




## Testing
To run the tests, run
```
dropdb casting_test
createdb casting_test
psql casting_test< casting_test.psql
python test_app.py
```