from datetime import datetime, UTC
import random
from app.extensions import db

class Reservation(db.Model):
    __tablename__ = 'reservations'

    reservation_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    time_slot = db.Column(db.DateTime, nullable=False)
    table_number = db.Column(db.Integer, nullable=False)
    guest_count = db.Column(db.Integer, nullable=False) # Added to hold number of guest
    reservation_name = db.Column(db.String(255), nullable=False) # Added reservation name in case it's different from customer
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC))

    __table_args__ = (
        db.UniqueConstraint('time_slot', 'table_number', name='unique_table_per_slot'),
    )

    @staticmethod
    def assign_random_table(time_slot):
        '''
        Assign a random available table (1-30) for the given time slot.
        Returns None if no tables are available.
        '''
        taken = {
            r.table_number
            for r in Reservation.query.filter_by(time_slot=time_slot).all()
        }
        available = [n for n in range(1, 31) if n not in taken]
        return random.choice(available) if available else None

    def __repr__(self):
        return f'<reservation {self.reservation_id}>'