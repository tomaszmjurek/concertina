from concertina.configs import connect_db

conn = connect_db()
cursor = conn.cursor()

from flask import Flask
from concertina.controllers.routes import init_blueprints

app = Flask(__name__)
init_blueprints(app)

