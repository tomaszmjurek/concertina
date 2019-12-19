from concertina.configs import Config, connect_db

conn = connect_db()
cursor = conn.cursor()

from flask import Flask
from concertina.controllers.routes import init_blueprints

app = Flask(__name__)
app.config.from_object(Config)
init_blueprints(app)

