from datetime import datetime, timedelta, UTC
import random
from app.extensions import db
from app.models import Customer, Reservation

def seed_data():
    '''
    Seeds the database with sample customers and reservations
    for initial testing and UI development.
    '''

    # --- Seed customers only if none exist ---
    if not Customer.query.first():
        print('Seeding customers...')
        customers = [
            Customer(
                customer_name='John Doe',
                customer_email='john.doe@example.com',
                phone_number='+639171234567',
                newsletter_signup=True,
                created_at=datetime.now(UTC)
            ),
            Customer(
                customer_name='Jane Smith',
                customer_email='jane.smith@example.com',
                phone_number='+639181112223',
                newsletter_signup=False,
                created_at=datetime.now(UTC)
            ),
            Customer(
                customer_name='Carlos Reyes',
                customer_email='carlos.reyes@example.com',
                phone_number='+639191234567',
                newsletter_signup=True,
                created_at=datetime.now(UTC)
            ),
        ]
        db.session.add_all(customers)
        db.session.commit()
        print('Customers seeded successfully.')
    else:
        print('Customers already exist. Skipping customer seeding.')

    # --- Seed reservations only if none exist ---
    if not Reservation.query.first():
        print('Seeding reservations...')
        customers = Customer.query.all()
        base_time = datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)

        for customer in customers:
            time_slot = base_time + timedelta(days=random.randint(0, 2))  # within the next 2 days
            table_number = Reservation.assign_random_table(time_slot)

            if table_number:
                reservation = Reservation(
                    customer_id=customer.customer_id,
                    reservation_name=customer.customer_name,
                    time_slot=time_slot.astimezone(UTC),
                    table_number=table_number,
                    guest_count=random.randint(2, 4),
                    created_at=datetime.now(UTC)
                )
                db.session.add(reservation)

        db.session.commit()
        print('Reservations seeded successfully.')
    else:
        print('Reservations already exist. Skipping reservation seeding.')