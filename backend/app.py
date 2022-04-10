from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from uuid import uuid4
from hashlib import sha256
from utils import calculate_circle_center, calculate_distance


app = Flask("backend")
CORS(app)

DISTANCE_THRESHOLD = 50
database = {}
# database = {
#     "123412": {
#         "uuid": "1234-123456-1234-1234",
#         "gameid": "123412",
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
        game_id = sha256(uuid.encode()).hexdigest()[:6]

        while game_id in database:
            uuid = str(uuid4())
            game_id = sha256(uuid.encode()).hexdigest()[:6]

        seeker_username = "seeker_username"
        response = {
            "uuid": uuid,
            "gameid": game_id,
            "seeker": seeker_username,
            "hiders": {}
        }
        database[game_id] = response
        return make_response(jsonify(response), 200)


@app.route("/seek/<uuid>", methods=["POST"])
def seek(uuid):
    if request.method == "POST":
        game_id = sha256(uuid.encode()).hexdigest()[:6]

        if game_id in database:
            game = database[game_id]
            latitude = request.args.get("latitude", 0)
            longitude = request.args.get("longitude", 0)
            game["latitude"] = latitude
            game["longitude"] = longitude

            seeker_position = (latitude, longitude)

            hiders = game["hiders"]
            for hider in hiders:
                hider_position = (hiders[hider]["latitude"], hiders[hider]["longitude"])
                distance = calculate_distance(seeker_position, hider_position)

                if distance < DISTANCE_THRESHOLD:
                    hiders[hider]["isFound"] = True
                else:
                    circle_center = calculate_circle_center(hider_position)
                    hiders[hider]["circle_center_latitude"] = circle_center[0]
                    hiders[hider]["circle_center_longitude"] = circle_center[1]

            database[game_id] = game
            return make_response(jsonify(game), 200)
        else:
            response = {
                "cod": "404", 
                "messaage": "game ID not found"
            }
            return make_response(jsonify(response), 404)


@app.route("/hide/<gameid>", methods=["POST"])
def create_hider(gameid):
    if request.method == "POST":
        if gameid in database:
            uuid = str(uuid4())
            hider_username = "hider"

            database[gameid]["hiders"][uuid] = {
                "username": hider_username,
                "isFound": False
            }

            response = {
                "uuid": uuid,
                "username": hider_username,
            }    
            return make_response(jsonify(response), 200)
        else:
            response = {
                "cod": "404", 
                "messaage": "game ID not found"
            }
            return make_response(jsonify(response), 404)


@app.route("/hider/<gameid>", methods=["POST"])
def broadcast_hider_location(gameid):
    if request.method == "POST":
        if gameid in database:
            game = database[gameid]
            seeker_username = game["seeker"]

            hider_uuid = request.args.get("uuid", 0)
            latitude = request.args.get("latitude", 0)
            longitude = request.args.get("longitude", 0)

            hider = game["hiders"][hider_uuid]
            hider["latitude"] = latitude
            hider["longitude"] = longitude

            hider_position = (latitude, longitude)
            seeker_position = (game["latitude"], game["longitude"])
            
            distance = calculate_distance(seeker_position, hider_position)
            
            if distance < DISTANCE_THRESHOLD:
                    hider["isFound"] = True

            response = {
                "username": seeker_username,
                "distance": distance,
                "isFound": hider["isFound"]
            }
            return make_response(jsonify(response), 200)
        else:
            response = {
                "cod": "404", 
                "messaage": "game ID not found"
            }
            return make_response(jsonify(response), 404)


if __name__ == "__main__":
    app.run("localhost", 5000)
