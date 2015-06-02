from flask import Flask, request
from flask_restful import Resource, Api

from model.player import Player

app = Flask(__name__)
api = Api(app)

players = {}


class PlayerController(Resource):
    def get(self):
        result = {}
        for id, player in players.items():
            result[id] = player.name

        return result

    def get(self, id):
        return {'id': id, 'name': players[id].name}

    def post(self):
        name = request.form['name']
        id = len(players) + 1
        players[id] = Player(name)

        return {'id': id, 'name': name}


api.add_resource(PlayerController, '/player/<int:id>', '/player')

if __name__ == '__main__':
    app.run(debug=True)
