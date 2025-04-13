from flask import render_template, request
from models import Booking


def register_routes(app, db):

    @app.route('/')
    def index():
        bookings = Booking.query.all()
        return str(bookings)