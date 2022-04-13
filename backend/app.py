from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from uuid import uuid4
from hashlib import sha256
from utils import random_username, calculate_circle_center, calculate_distance

app = Flask("backend")
CORS(app)

DISTANCE_THRESHOLD = 50
database = {}
# database = {
#     "123412": {
#         "uuid": "1234-123456-1234-1234",
#         "game_id": "123412",
#         "seeker": "seeker",
#         "hiders": {},
#         "latitude": "30",
#         "longitude": "20"
#     }
# }


@app.route("/seek", methods=["POST"])
def create_game():
    if request.method == "POST":
        uuid = str(uuid4())
        game_id = sha256(uuid.encode()).hexdigest()[:6].lower()

        while game_id in database:
            uuid = str(uuid4())
            game_id = sha256(uuid.encode()).hexdigest()[:6].lower()

        seeker_username = random_username(game_id)
        response = {
            "uuid": uuid,
            "game_id": game_id,
            "seeker": seeker_username,
            "hiders": {}
        }

        database[game_id] = response
        return make_response(jsonify(response), 200)


@app.route("/seek/<uuid>", methods=["POST"])
def seek(uuid):
    if request.method == "POST":
        game_id = sha256(uuid.encode()).hexdigest()[:6].lower()

        if game_id in database:
            game = database[game_id]

            latitude = float(request.args.get("latitude", 0))
            longitude = float(request.args.get("longitude", 0))

            game["latitude"] = latitude
            game["longitude"] = longitude

            seeker_position = (latitude, longitude)

            response = game.copy()
            response["hiders"] = {}

            for hider in game["hiders"]:
                hider_position = (
                    game["hiders"][hider]["latitude"],
                    game["hiders"][hider]["longitude"]
                )

                distance = calculate_distance(seeker_position, hider_position)

                response["hiders"][hider] = game["hiders"][hider].copy()

                if distance < DISTANCE_THRESHOLD or game["hiders"][hider]["found"]:
                    game["hiders"][hider]["found"] = True
                    response["hiders"][hider]["found"] = True
                else:
                    circle_center = calculate_circle_center(hider_position)
                    response["hiders"][hider]["latitude"] = circle_center[0]
                    response["hiders"][hider]["longitude"] = circle_center[1]

            database[game_id] = game
            return make_response(jsonify(response), 200)
        else:
            response = {
                "message": "game ID not found"
            }
            return make_response(jsonify(response), 404)


@app.route("/hide/<game_id>", methods=["POST"])
def create_hider(game_id):
    if request.method == "POST":
        game_id = game_id.lower()
        if game_id in database:
            uuid = str(uuid4())

            hider_username = random_username(game_id)

            database[game_id]["hiders"][uuid] = {
                "username": hider_username,
                "found": False,
                "latitude": 0,
                "longitude": 0
            }

            response = {
                "uuid": uuid,
                "username": hider_username,
            }
            return make_response(jsonify(response), 200)
        else:
            response = {
                "message": "game ID not found"
            }
            return make_response(jsonify(response), 404)


@app.route("/hider/<game_id>", methods=["POST"])
def broadcast_hider_location(game_id):
    if request.method == "POST":
        game_id = game_id.lower()
        if game_id in database:
            game = database[game_id]
            seeker_username = game["seeker"]

            hider = request.args.get("uuid", 0)
            latitude = float(request.args.get("latitude", 0))
            longitude = float(request.args.get("longitude", 0))

            game["hiders"][hider]["latitude"] = latitude
            game["hiders"][hider]["longitude"] = longitude

            hider_position = (latitude, longitude)
            seeker_position = (game["latitude"], game["longitude"])

            distance = calculate_distance(seeker_position, hider_position)

            if distance < DISTANCE_THRESHOLD:
                game["hiders"][hider]["found"] = True

            database[game_id] = game

            response = {
                "username": seeker_username,
                "distance": distance,
                "found": game["hiders"][hider]["found"]
            }
            return make_response(jsonify(response), 200)
        else:
            response = {
                "message": "game ID not found"
            }
            return make_response(jsonify(response), 404)


if __name__ == "__main__":
    app.run("localhost", 5000)
