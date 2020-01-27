from concertina.controllers.concerts_controller import concerts_bp
from concertina.controllers.bands_controller import bands_bp
from concertina.controllers.festivals_controller import festivals_bp
from concertina.controllers.genres_controller import genres_bp
from concertina.controllers.instruments_controller import instruments_bp
from concertina.controllers.musicians_controller import musicians_bp
from concertina.controllers.albums_controller import albums_bp
from concertina.controllers.places_controller import places_bp
from concertina.controllers.songs_controller import songs_bp
from concertina.controllers.awards_controller import awards_bp
from concertina.controllers.award_receptions_controller import award_receptions_bp
from concertina.controllers.appearnaces_controller import app


def init_blueprints(app):
    app.register_blueprint(concerts_bp)
    app.register_blueprint(bands_bp)
    app.register_blueprint(musicians_bp)
    app.register_blueprint(festivals_bp)
    app.register_blueprint(albums_bp)
    app.register_blueprint(songs_bp)
    app.register_blueprint(instruments_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(genres_bp)
    app.register_blueprint(awards_bp)
    app.register_blueprint(award_receptions_bp)