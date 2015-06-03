from flask import Flask
from flask_restful import Api
from api.controller import PlayerController

app = Flask(__name__)
api = Api(app)

PlayerController.load(api)

if __name__ == '__main__':
    app.run(debug=True)
