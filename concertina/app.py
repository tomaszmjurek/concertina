from flask import Flask
from concertina.configs import Config, init_extensions
from concertina.controllers.routes import init_blueprints

app = Flask(__name__)
app.config.from_object(Config)

init_extensions(app)
init_blueprints(app)

from . import shell_context