from concertina.configs import Config, connect_db
from psycopg2.extras import RealDictCursor

conn = connect_db()
cursor = conn.cursor(cursor_factory=RealDictCursor)

from flask import Flask
from concertina.controllers.routes import init_blueprints

app = Flask(__name__)
app.config.from_object(Config)
init_blueprints(app)

@app.teardown_appcontext
def close_db(error):
    conn.close()
