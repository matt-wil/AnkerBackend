from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Booking(db.Model):
    __tablename__ = 'bookings'

    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    artist_id = db.Column(db.Integer, nullable=False)
    service_id = db.Column(db.Integer, nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=False)
    notes = db.Column(db.String)
    booking_status = db.Column(db.String(50), default="pending")
    created_at = db.Column(db.Datetime, default=func.now())

    user = relationship("User", back_populates="bookings")
    artist = relationship("Artist", back_populates="bookings")
    service = relationship("Service", back_populates="bookings")

    def __repr__(self):
        return f"Status: {self.booking_status}\n\tBooking with {self.user_id} at {self.booking_time} on the {self.booking_date}"


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    registration_date = db.Column(db.Datetime, default=func.now())

    client = relationship("Client", back_populates="user", uselist=False)

    def __repr__(self):
        return f"User Details\n\tId: {self.user_id}\n\tUsername: {self.username}\n\tEmail: {self.email}\n\tRegistration Date: {self.registration_date}"


class Client(db.Model):
    __tablename__ = 'clients'

    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.Text)
    email = db.Column(db.String(100), unique=True, nullable=False)
    consent_signed_date = db.Column(db.Date)
    preferences = db.Column(db.Text)

    user = relationship("User", back_populates="client")

    def __repr__(self):
        return f"Client Details\n\tClient Id: {self.client_id}\n\tUser Id: {self.user_id}\n\tName: {self.first_name} {self.last_name}\n\tEmail: {self.email}\n\tAddress: {self.address}\n\tContact: {self.phone_number}"


class Artist(db.Model):
    __tablename__ = "images"

    artist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    specialities = db.Column(db.Text)
    profile_image = db.Column(db.String(255))  # url to the static/images/artists
    is_active = db.Column(db.Boolean, default=True)
    contact_email = db.Column(db.String(100))
    social_media_links = db.Column(db.Text)

    portfolio_images = relationship("PortfolioImage", back_populates="artist")
    bookings = relationship("Booking", back_populates="artist")

    def __repr__(self):
        return f"Artist Details\n\tName: {self.name}\n\tStatus: {self.is_active}"


class Service(db.Model):
    __tablename__ = "services"

    service_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))

    booking = relationship("Booking", back_populates="service")

    def __repr__(self):
        return f"Service Details\n\tID: {self.service_id}\n\tName: {self.name}\n\tPrice: {self.price}"


class PortfolioImages(db.Model):
    __tablename__ = 'portfolio_images'

    image_id = db.Column(db.Integer, primary_key=True, nullable=True)
    artist_id = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    upload_date = db.Column(db.Datetime, default=func.now())

    artist = relationship("Artist", back_populates="portfolio_images")

    def __repr__(self):
        return f"Artist: {self.artist_id}\nImage url: {self.image_url}"


# to be Initialized at a later date
# class BlogPosts(db.Model):
#     __tablename__ = 'blog_posts'










