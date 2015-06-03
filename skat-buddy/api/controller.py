from flask import request
from flask_restful import Resource

from model.player import Player


players = {}
# ------------------------------------------------------------
# Player controller class
# ------------------------------------------------------------
class PlayerController(Resource):

    @staticmethod
    def load(api):
        api.add_resource(PlayerController, '/player/<int:id>', '/player')

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
