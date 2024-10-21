''' Initialize the app '''

from flask import Flask

import uuid

from src.database import database
from src.api.blueprints.auth import bp as auth_bp
from src.api.blueprints.goal import bp as goal_bp
from src.api.blueprints.graph import bp as graph_bp
from src.api.blueprints.blueprint import bp as main_bp
from src.api import routes


def create_app():
    ''' Create and configure the app '''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        CONFIG_FILE="src/api/app.ini",
        SECRET_KEY=str(uuid.uuid4())
    )

    database.init_app(app)
    
    routes.init_routes(app)

    app.register_blueprint(main_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(goal_bp, url_prefix="/goal")
    app.register_blueprint(graph_bp, url_prefix="/graph")

    return app

if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=8000, debug=True)
