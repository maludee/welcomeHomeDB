import os
import pymysql
import datetime

pymysql.install_as_MySQLdb()

from flask import Flask, render_template, request

# from flask_mysqldb import MySQL
from flask_login import LoginManager, login_required, current_user
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
        if request.method == "POST":
            item_id = request.form["item_id"]
            database = db.get_db()
            cursor = database.cursor()
            query = f"""SELECT itemID, pieceNum, pDescription, roomNum, shelfNum, pNotes 
                    FROM Piece 
                    WHERE itemID = {item_id}"""
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            return render_template("find_item.html", data=data, item_id=item_id)
        else:
            return render_template("find_item.html")

    @app.route("/find_order", methods=("GET", "POST"))
    @login_required
    def find_order():
        if request.method == "POST":
            order_id = request.form["order_id"]
            database = db.get_db()
            cursor = database.cursor()
            query = f"""SELECT orderID, 
                               itemID,
                               pieceNum, 
                               pDescription, 
                               roomNum, 
                               shelfNum, 
                               shelfDescription,
                               mainCategory,
                               subCategory
                        FROM Piece
                        NATURAL JOIN Item
                        NATURAL JOIN location
                        NATURAL JOIN ItemIn
                        WHERE orderID = {order_id}"""
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            return render_template("find_order.html", data=data, order_id=order_id)
        else:
            return render_template("find_order.html")

    @app.route("/check_donor", methods=("GET", "POST"))
    @login_required
    def check_donor():
        if request.method == "POST":
            # assuming here that prompt user for donor_id means the donor's username
            # since I didn't see a donor_id in the schema
            donor_username = request.form["donor_username"]
            database = db.get_db()
            cursor = database.cursor()
            query = f"""SELECT username, roleID
                        FROM Person
                        NATURAL JOIN Act
                        WHERE username = '{donor_username}'
                        AND roleID = 3
                    """
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            if data == []:
                return render_template(
                    "donation/check_donor.html",
                    data=data,
                    donor_username=donor_username,
                )
            else:
                return render_template(
                    "donation/accept_donation.html",
                    data=data,
                    donor_username=donor_username,
                )
        else:
            return render_template("donation/check_donor.html")

    @app.route("/accept_donation", methods=("GET", "POST"))
    @login_required
    def accept_donation():
        if request.method == "POST":
            donor_username = request.form["donor_username"]
            iDescription = request.form["item_description"]
            photo = request.form["photo"]
            color = request.form["color"]
            material = request.form["material"]
            if request.form["number_of_pieces"] == "1":
                hasPieces = 0
            else:
                hasPieces = 1
            mainCategory = request.form["mainCategory"]
            subCategory = request.form["subCategory"]
            if request.form["isNew"] == "FALSE":
                isNew = 0
            else:
                isNew = 1
            print(iDescription, photo)
            database = db.get_db()
            cursor = database.cursor()
            cursor.execute(
                "INSERT INTO Item (iDescription, photo, color, isNew, hasPieces, material, mainCategory, subCategory) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    iDescription,
                    photo,
                    color,
                    isNew,
                    hasPieces,
                    material,
                    mainCategory,
                    subCategory,
                ),
            )
            database.commit()
            # get the item id for the item we just insterted
            cursor.execute(f"SELECT * FROM Item ORDER BY itemID DESC LIMIT 1")
            itemID = cursor.fetchone()
            itemID = itemID[0]
            donateDate = datetime.date.today().strftime("%Y-%m-%d")
            # fill in donation info in donatedBy table
            cursor.execute(
                "INSERT INTO DonatedBy (ItemID, userName, donateDate)"
                "VALUES (%s, %s, %s)",
                (itemID, donor_username, donateDate),
            )
            database.commit()

            # get the rooms and shelves from location, this will be for populating the html
            cursor.execute("SELECT roomNum, shelfNum FROM Location") 
            res = cursor.fetchall()
            rooms = sorted([i[0] for i in res])
            shelves = sorted([i[1] for i in res])
            print(rooms, shelves)
            cursor.close()
            return render_template(
                "donation/store_pieces.html",
                donor_username=donor_username,
                number_of_pieces=int(request.form["number_of_pieces"]),
                rooms=rooms,
                shelves=shelves,
                itemID = itemID
            )
        else:
            return render_template("donation/accept_donation.html")

    @app.route("/store_pieces", methods=("GET", "POST"))
    @login_required
    def store_pieces():
        if request.method == "POST":
            itemID = request.form["itemID"]
            number_of_pieces = int(request.form['number_of_pieces'])
            database = db.get_db()
            cursor = database.cursor()

            # this should let me collect all of the piece information and send to db 
            for i in range(1, number_of_pieces + 1):
                pieceNum = request.form[f'pieceNum_{i}']
                pDescription = request.form[f'pDescription_{i}']
                length = request.form[f'length_{i}']
                width = request.form[f'width_{i}']
                height = request.form[f'height_{i}']
                roomNum = request.form[f'roomNum_{i}']
                shelfNum = request.form[f'shelfNum_{i}']
                pNotes = request.form[f'pNotes_{i}']

            cursor.execute(
                "INSERT INTO Piece (ItemID, pieceNum, pDescription, length, width, height, roomNum, shelfNum, pNotes)" 
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                itemID,
                pieceNum,
                pDescription,
                length,
                width,
                height,
                roomNum,
                shelfNum,
                pNotes
                ),
            )
            database.commit()

        cursor.close()
        return "All done" 
   

    return app
