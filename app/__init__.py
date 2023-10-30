from flask import Flask
from config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
jwt = JWTManager(app)

from app import routes