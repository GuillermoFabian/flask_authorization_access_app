# Coffee Shop 


### Auth0 account
```
AUTH0_DOMAIN = 'dev-fkoly682.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffee'
```

### POSTman
* Exported collection with configured tokens can be found at: `/backend/local_token.postman_collection_local.json`


### Backend

* Added Auth0 functionalities
* Implemented RESTful endpoints
* Implemented error handlers
* I've used [black](https://black.readthedocs.io/en/stable/) to enforce python code style

#### Running the app

1. Install dependencies with `pip install -r backend/requirements.txt`
2. Set the `FLASK_APP` variable running `export FLASK_APP=api.py` 
3. Run the app with `flask run --reload`

### Frontend 

* Added the Auth0 variables on `environment.ts` file
* Guarantee that the frontend can be launched upon an `ionic serve` command and the login/token retrieval are functional


### .gitignore
* Added virtual enviroment folder
* Added node modules