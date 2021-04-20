import random

import flask_sqlalchemy
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

import util.logging
from util.logging import log_decorator
import logging

rootlogger = util.logging.get_root_logger()
logger = logging.getLogger(__name__)

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
        logger.debug(f"dict: {cafe_dict}")
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
        except AttributeError as ae:     print(ae)

    @log_decorator
    def get_json(self):
        # cafedict = self.manual_dict()
        # cafedict = self._dict()
        cafedict = self.get_dict()
        json_cafe = jsonify(cafedict)
        logger.debug(json_cafe)
        return json_cafe


@app.route("/")
@log_decorator
def home():
    return render_template("index.html")


@app.route("/random", methods=["GET"])
@log_decorator
def get_randomcafe():
    cafes = db.session.query(Cafe).all()
    logger.debug(cafes)
    cafe = random.choice(cafes)
    logger.debug(cafe)
    # return render_template("index.html")
    return cafe.get_json()


## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
