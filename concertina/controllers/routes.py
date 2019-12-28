from concertina.controllers.concerts_controller import concerts_bp


def init_blueprints(app):
    app.register_blueprint(concerts_bp)
