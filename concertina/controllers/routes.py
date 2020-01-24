from concertina.controllers.concerts_controller import concerts_bp
from concertina.controllers.bands_controller import bands_bp
from concertina.controllers.musicians_controller import musicians_bp


def init_blueprints(app):
    app.register_blueprint(concerts_bp)
    app.register_blueprint(bands_bp)
    app.register_blueprint(musicians_bp)