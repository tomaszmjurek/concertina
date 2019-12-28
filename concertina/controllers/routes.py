from concertina.controllers.controller import main_bp


def init_blueprints(app):
    app.register_blueprint(main_bp)
