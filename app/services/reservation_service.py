from app.models import Customer, Reservation
from app.extensions import db

def create_reservation(customer_data, time_slot):
    # Create or find customer
    customer = Customer.query.filter_by(customer_email=customer_data['customer_email']).first()
    if not customer:
        customer = Customer(**customer_data)
        db.session.add(customer)
        db.session.commit()

    # Assign table
    assigned_table = Reservation.assign_random_table(time_slot)
    if not assigned_table:
        return {'success': False, 'message': 'All tables are full for this time slot.'}

    reservation = Reservation(customer_id=customer.customer_id, time_slot=time_slot, table_number=assigned_table)
    db.session.add(reservation)
    db.session.commit()

    return {'success': True, 'message': f'Table {assigned_table} reserved successfully!'}
