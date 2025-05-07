from .extensions import db, pwd_context
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Enum
from sqlalchemy.ext.hybrid import hybrid_property
import enum


class BookingStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"


class Booking(db.Model):
    __tablename__ = 'bookings'
    __table_args__ = (
        db.UniqueConstraint('artist_id', 'booking_date', 'booking_time', name='uq_artist_booking_slot'),
    )

    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.client_id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=False)
    notes = db.Column(db.String)
    booking_status = db.Column(Enum(BookingStatus), default=BookingStatus.pending, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

    client = relationship("Client", back_populates="bookings")
    artist = relationship("Artist", back_populates="bookings")
    service = relationship("Service", back_populates="bookings")

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "client_id": self.client_id,
            "artist_id": self.artist_id,
            "service_id": self.service_id,
            "booking_date": self.booking_date,
            "booking_time": self.booking_time,
            "notes": self.notes,
            "booking_status": self.booking_status,
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"Status: {self.booking_status}\n\tBooking with {self.client_id} at {self.booking_time} on the {self.booking_date}"


class Client(db.Model):
    __tablename__ = 'clients'

    client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.Text)
    email = db.Column(db.String(100), unique=True, nullable=False)
    consent_signed_date = db.Column(db.Date)
    preferences = db.Column(db.Text)

    bookings = relationship("Booking", back_populates="client")

    def to_dict(self):
        return {
            "client_id": self.client_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "address": self.address,
            "email": self.email,
            "consent_signed_date": self.consent_signed_date,
            "preferences": self.preferences
        }

    def __repr__(self):
        return f"Client Details\n\tClient Id: {self.client_id}\n\tUser Id: {self.user_id}\n\tName: {self.first_name} {self.last_name}\n\tEmail: {self.email}\n\tAddress: {self.address}\n\tContact: {self.phone_number}"


class Artist(db.Model):
    __tablename__ = "artists"

    artist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    profession = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    specialties = db.Column(db.Text)
    profile_image = db.Column(db.String(255))  # url to the static/images/artists
    is_active = db.Column(db.Boolean, default=True)
    contact_email = db.Column(db.String(100))
    social_media_links = db.Column(db.JSON, default=dict)

    portfolio_images = relationship("PortfolioImage", back_populates="artist")
    bookings = relationship("Booking", back_populates="artist")

    def to_dict(self):
        return {
            "artist_id": self.artist_id,
            "name": self.name,
            "profession": self.profession,
            "bio": self.bio,
            "specialties": self.specialties,
            "profile_image": self.profile_image,
            "is_active": self.is_active,
            "contact_email": self.contact_email,
            "social_media_links": self.social_media_links
        }

    def __repr__(self):
        return f"Artist Details\n\tName: {self.name}\n\tStatus: {self.is_active}"


class Service(db.Model):
    __tablename__ = "services"

    service_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))

    bookings = relationship("Booking", back_populates="service")

    def to_dict(self):
        return {
            "service_id": self.service_id,
            "name": self.name,
            "description": self.description,
            "duration": self.duration,
            "price": self.price
        }

    def __repr__(self):
        return f"Service Details\n\tID: {self.service_id}\n\tName: {self.name}\n\tPrice: {self.price}"


class PortfolioImage(db.Model):
    __tablename__ = 'portfolio_images'

    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    upload_date = db.Column(db.DateTime, default=func.now())

    artist = relationship("Artist", back_populates="portfolio_images")

    def to_dict(self):
        return {
            "image_id": self.image_id,
            "artist_id": self.artist_id,
            "image_url": self.image_url,
            "description": self.description,
            "category": self.category,
            "upload_date": self.upload_date
        }

    def __repr__(self):
        return f"Artist: {self.artist_id}\nImage url: {self.image_url}"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)


class TokenBlockList(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    token_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    revoked_at = db.Column(db.DateTime)
    expires = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User")











