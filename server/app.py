# server/app.py

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

# start building your API here
# create a route to get all the games
@app.route("/games")
def games():
    # Initializing games with an empty array
    games = []

    #  looping through the games to get each game 
    for game in Game.query.all():
        #  creating a dictionary object using the to_dict() method
        game_dict = game.to_dict()
        #  appending the game_obj to the games
        games.append(game_dict)
    response = make_response(jsonify(games, 200, {"Content-type":"application/json"}))
    return response

#  create a route that gets a specfic game by the id 
@app.route("/games/<int:id>")
def game_by_id(id):
    # querying through the data to get a game with a specific id
    game = Game.query.filter(Game.id == id).first()

    #  creating a dictionary object using the to_dict() method
    game_dict = game.to_dict()

    # creating a response
    response = make_response(game_dict, 200)
    return response

# create a route that gets the specific users of a certain game
@app.route("/games/users/<int:id>")
def game_users_by_id(id):
    # getting a game using the id
    game = Game.query.filter_by(id = id).first()

    #  Initializing the users with an empty array
    users = []

    #  creating a loop to get the users for a specific game
    for user in game.users:
        # creating a dictionary usig the to_dict method and using serialization rules to avoid maximum recurssion error
        user_dict = user.to_dict(rules = ("-reviews", ))
        users.append(user_dict)
    
    # creating a response
    response = make_response(users, 200)
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)

