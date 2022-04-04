from flask import Flask, request
from json import dumps, loads
from uuid import uuid4
from hashlib import sha256


app = Flask("backend")


database = {}


@app.route("/seek", methods=["POST"])
def create_game():
    if request.method == "POST":
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
        return dumps(response)


@app.route("/seek/<uuid>")
def seek(uuid):
    if request.method == "GET":
        game_id = sha256(uuid.encode()).hexdigest()[:6]
        if game_id in database:
            game = database[game_id]
            latitude = request.args.get("latitude", 0)
            longitude = request.args.get("longitude", 0)
            game["latitude"] = latitude
            game["longitude"] = longitude
            # for hider in game["hiders"]:
            #     # if not found:
            #     #     # TODO: Calculate the hiders circle center
            #     # else:
            #     #     # TODO: Send true location
            database[game_id] = game
            return dumps(game)
        else:
            return ""


@app.route("/hide/<gameid>", methods=["GET"])
def create_hider(gameid):
    return ""


@app.route("/hide/<gameid>", methods=["POST"])
def broadcast_hider_location(gameid):
    if request.method == "POST":
        hider_uuid = request.args.get("uuid", 0)
        latitude = request.args.get("latitude", 0)
        longitude = request.args.get("longitude", 0)
        return ""


if __name__ == "__main__":
    app.run("localhost", 5000)
