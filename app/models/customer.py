from datetime import datetime, UTC
from app.extensions import db

class Customer(db.Model):
    __tablename__ = 'customers'

    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(255), nullable=False)
    customer_email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    newsletter_signup = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC))

    reservations = db.relationship('Reservation', backref='customer', lazy=True)

    def __repr__(self):
        return f'<customer {self.customer_name}>'