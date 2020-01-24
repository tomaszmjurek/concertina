from concertina.controllers.concerts_controller import concerts_bp
from concertina.controllers.bands_controller import bands_bp


def init_blueprints(app):
    app.register_blueprint(concerts_bp)
    app.register_blueprint(bands_bp)