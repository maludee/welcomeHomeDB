import os
import pymysql

pymysql.install_as_MySQLdb()

from flask import Flask

# from flask_mysqldb import MySQL
from flask_login import LoginManager, login_required
from dotenv import load_dotenv
load_dotenv()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )
    app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
    app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
    app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
    app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
    app.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from . import db

    db.init_app(app)
    from .auth import create_auth_blueprint

    auth_bp = create_auth_blueprint(login_manager)
    app.register_blueprint(auth_bp)
    app.add_url_rule("/", endpoint="auth.login")

    #  a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"
    
    @app.route("/find_item", methods=("GET", "POST"))
    @login_required
    def find_item():
        return "Finding an item..."
    
    @app.route("/find_order", methods=("GET", "POST"))
    @login_required
    def find_order():
        return "Finding an order..."
    
    @app.route("/accept_donation", methods=("GET", "POST"))
    @login_required
    def accept_donation():
        return "Accepting a donation..."

    return app
