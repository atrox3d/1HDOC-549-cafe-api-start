import random

import flask_sqlalchemy
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

import util.logging
from util.logging import log_decorator
import logging

rootlogger = util.logging.get_root_logger(
    format_string='%(asctime)s | %(levelname)-8s | %(name)-15s | %(funcName)15s() | %(message)s'

)
logger = logging.getLogger(__name__)

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    @log_decorator
    def __init__(self, **kwargs):
        for col in self.__table__.columns:
            logger.info(f"{col.name}:{col.type}={getattr(self, col.name)}")
            if str(col.type) == "BOOLEAN":
                logger.info("BOOLEAN detected")
                logger.info(kwargs[col.name])
                if kwargs[col.name].lower() in [ "true", "1" ]:
                    kwargs[col.name] = True
                else:
                    kwargs[col.name] = False
        super().__init__(**kwargs)

    @log_decorator
    def manual_dict(self):
        """
        manual conversion of object to dict

        grants finer control over dict but needs to be updated with the class

        :return:
        """
        thedict = {
            "id": self.id,
            "name": self.name,
            "map_url": self.map_url,
            "img_url": self.img_url,
            "location": self.location,
            "seats": self.seats,
            "has_toilet": self.has_toilet,
            "has_wifi": self.has_wifi,
            "has_sockets": self.has_sockets,
            "can_take_calls": self.can_take_calls,
            "coffee_price": self.coffee_price,
        }
        logger.debug(f"manual dict: {thedict}")
        return thedict

    # works
    @log_decorator
    def get_dict(self):
        """
        dictionary comprehension as stated in examples

        always returns all fields and keeps itself up to date

        :return:
        """
        cafe_dict = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        logger.debug(f"cafe_dict: {cafe_dict}")
        return cafe_dict

    # works
    @log_decorator
    def _dict(self):
        """
        hack to get dict

        :return:
        """
        try:
            selfdict = self.__dict__.copy()
            del selfdict['_sa_instance_state']
            logger.debug(f"self.__dict__: {selfdict}")
            return selfdict
        except Exception as e:
            print(e)

    # does not work
    @log_decorator
    def to_dict(self):
        """
        does not work: TypeError

        :return:
        """
        try:
            row_as_dict = dict(self)
            logger.debug(f"row_as_dict: {row_as_dict}")
            return row_as_dict
        except TypeError as te:
            logger.debug(te)

    # does not work
    @log_decorator
    def as_dict(self):
        """
        does not work: AttributeError

        :return:
        """
        try:
            asdict = self._asdict()
            print("self._asdict(): ", asdict)
            return asdict
        except AttributeError as ae:
            print(ae)


@app.route("/")
@log_decorator
def home():
    """
    route to /index.html

    :return:
    """
    return render_template("index.html")


################################################################################
#  HTTP GET - Read Record
################################################################################

@app.route("/random")
@log_decorator
def get_randomcafe():
    """
    route to /random

    selects a random cafe from db

    :return: json of selected cafe
    """
    cafes = db.session.query(Cafe).all()
    logger.debug(cafes)
    cafe = random.choice(cafes)
    logger.debug(cafe)
    return jsonify(cafe.get_dict())


@app.route("/all")
@log_decorator
def get_allcafes():
    """
    route to /all

    :return: json of all cafes in the db
    """
    cafes = db.session.query(Cafe).all()
    logger.debug(cafes)
    # json_cafes = { "cafes": [cafe.get_json() for cafe in cafes] }
    all_cafes = [cafe.get_dict() for cafe in cafes]
    return jsonify(all_cafes=all_cafes)


################################################################################
# https://stackoverflow.com/a/6345834
################################################################################
# My personal rule of thumb that the PathParam leads upto the entity type
# that you are requesting.
#
# /Invoices             // all invoices
# /Invoices?after=2011  // a filter on all invoices
#
# /Invoices/52          // by 52
# /Invoices/52/Items    // all items on invoice 52
# /Invoices/52/Items/1  // Item 1 from invoice 52
#
# /Companies/{company}/Invoices?sort=Date
# /Companies/{company}/Invoices/{invoiceNo} // assuming that the invoice only
# unq by company?
# To quote Mr Rowe:
# Path parameters for grouping data, query parameters for filtering
################################################################################

@app.route("/search")
@log_decorator
def search_cafes():
    """
    route to /search?location=<location>

    searches for a cafe in the db having location==<location>

    :return: json of the matching cafes
    """
    location = request.args.get("location")
    logger.debug(location)
    cafes = db.session.query(Cafe).filter_by(location=location)
    logger.debug(cafes)
    logger.debug(cafes.count())

    if not cafes.count():
        return jsonify(error="Fab not Found (check THE BOX)")
    else:
        all_cafes = [cafe.get_dict() for cafe in cafes]
        return jsonify(matching=all_cafes)


@app.route("/search/<location>")
@log_decorator
def find_cafes(location):
    """
    route to /search/<location>

    restful version of search?

    :param location: part of url
    :return: json of the matching cafes
    """
    logger.debug(f"location: {location}")
    cafes = db.session.query(Cafe).filter_by(location=location)
    logger.debug(cafes)
    logger.debug(f"cafes count: {cafes.count()}")

    if not cafes.count():
        return jsonify(error=f"{location} not Found (check THE BOX)")
    else:
        found_cafes = [cafe.get_dict() for cafe in cafes]
        return jsonify(matching=found_cafes)


################################################################################
# DONE: https://www.udemy.com/course/100-days-of-code/learn/lecture/22653535#questions
# DONE: install postman
# DONE: test endpoints
# DONE: document endpoints
################################################################################

################################################################################
# HTTP POST - Create Record
################################################################################
# TODO: https://www.udemy.com/course/100-days-of-code/learn/lecture/22647101#questions
# TODO: implement /add route
# DONE: create new cafes with postman
# TODO: OR use a form instead of postman
################################################################################
@app.route("/add", methods=["POST"])
@log_decorator
def add_cafe():
    logger.debug(request.form)
    # for name, value in request.form.items():
    #     logger.debug(f"request.form[{name}]={value}")
    cafe_dict = request.form.to_dict()
    logger.debug(f"request.form.to_dict(): {cafe_dict}")
    # same thing
    cafe = Cafe(**cafe_dict)
    cafe = Cafe(**request.form.to_dict())
    logger.debug(f"new cafe: {cafe}")
    db.session.add(cafe)
    try:
        db.session.commit()
        return jsonify(response=dict(success="succesful added the new cafè"))
    except Exception as e:
        return jsonify(response=dict(error="could not add cafè"))

################################################################################
# HTTP PUT/PATCH - Update Record
################################################################################
@app.route("/update-price/<cafeid>/<price>")
@log_decorator
def update_price(cafeid, price):
    logger.debug(f"cafeid: {cafeid}")
    logger.debug(f"price : {price}")

    return f"{cafeid}, {price}"


################################################################################
# HTTP DELETE - Delete Record
################################################################################


if __name__ == '__main__':
    app.run(debug=True)
