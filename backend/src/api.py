import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

"""
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
"""
db_drop_and_create_all()

# ROUTES
"""
@TODO implement endpoint GET /drinks
"""


@app.route("/drinks", methods=["GET"], endpoint="get_drinks")
def drinks():

    try:
        return (
            json.dumps(
                {
                    "success": True,
                    "drinks": [drink.short() for drink in Drink.query.all()],
                }
            ),
            200,
        )
    except:
        return json.dumps({"success": False, "error": "An error occurred"}), 500


"""
@TODO implement endpoint POST /drinks
"""


@app.route("/drinks", methods=["POST"], endpoint="post_drink")
@requires_auth("post:drinks")
def drinks(payload):

    data = dict(request.form or request.json or request.data)
    drink = Drink(
        title=data.get("title"),
        recipe=data.get("recipe")
        if type(data.get("recipe")) == str
        else json.dumps(data.get("recipe")),
    )
    try:
        drink.insert()
        return jsonify({"success": True, "drink": drink.long()}), 200
    except:
        return json.dumps({"success": False, "error": "An error occurred"}), 500


"""
@TODO implement endpoint GET /drinks-detail 
"""


@app.route("/drinks-detail", methods=["GET"], endpoint="drinks_detail")
@requires_auth("get:drinks-detail")
def drinks_detail(payload):
    try:
        return (
            json.dumps(
                {
                    "success": True,
                    "drinks": [drink.long() for drink in Drink.query.all()],
                }
            ),
            200,
        )
    except:
        return json.dumps({"success": False, "error": "An error occurred"}), 500


"""
@TODO implement endpoint PATCH /drinks/<id> 
"""


@app.route("/drinks/<id>", methods=["PATCH"], endpoint="patch_drink")
@requires_auth("patch:drinks")
def drinks(payload, id):

    try:
        data = dict(request.form or request.json or request.data)
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink:
            drink.title = data.get("title") if data.get("title") else drink.title
            recipe = data.get("recipe") if data.get("recipe") else drink.recipe
            drink.recipe = recipe if type(recipe) == str else json.dumps(recipe)
            drink.update()
            return json.dumps({"success": True, "drinks": [drink.long()]}), 200
        else:
            return (
                json.dumps(
                    {
                        "success": False,
                        "error": "Drink #" + id + " not found to be edited",
                    }
                ),
                404,
            )
    except:
        return jsonify({"success": False, "error": "An error occurred"}), 500


"""
@TODO implement endpoint DELETE /drinks/<id>
"""


@app.route("/drinks/<id>", methods=["DELETE"], endpoint="delete_drink")
@requires_auth("patch:drinks")
def drinks(payload, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink:
            drink.delete()
            return json.dumps({"success": True, "drink": id}), 200
        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Drink #" + id + " not found to be deleted",
                    }
                ),
                404,
            )
    except:
        return json.dumps({"success": False, "error": "An error occurred"}), 500


## Error Handling
"""
Example error handling for unprocessable entity
"""


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": error.error}), 422


@app.errorhandler(400)
def unprocessable(error):
    return jsonify({"success": False, "error": 400, "message": error.error}), 400


"""
@TODO implement error handler for Not Found 
"""


@app.errorhandler(404)
def unprocessable(error):
    """
    Propagates the formatted 404 error to the response
    """
    return jsonify({"success": False, "error": 404, "message": error.error}), 404


"""
@TODO implement error handler for AuthError - DONE 
"""


@app.errorhandler(AuthError)
def handle_auth_error(error):

    response = jsonify(error.error)
    response.status_code = error.status_code
    return response
