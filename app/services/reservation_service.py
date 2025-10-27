from datetime import datetime, UTC
from app.models import Customer, Reservation
from app.extensions import db

def create_reservation(customer_data, time_slot):
    # Create or find customer
    customer = Customer.query.filter_by(customer_email=customer_data['customer_email']).first()
    is_new_customer = False
    if not customer:
        customer = Customer(**customer_data)
        db.session.add(customer)
        db.session.commit()
        is_new_customer = True
        
    customer_info = {
        'customer_name': customer.customer_name,
        'customer_email': customer.customer_email,
        'is_new_customer': is_new_customer
    }

    # Assign table
    assigned_table = Reservation.assign_random_table(time_slot)
    if not assigned_table:
        return {
            'success': False, 
            'message': 'All tables are full for this time slot.',
            'customer': customer_info
        }

    reservation = Reservation(customer_id=customer.customer_id, time_slot=time_slot, table_number=assigned_table)
    db.session.add(reservation)
    db.session.commit()

    return {
        'success': True, 
        'message': f'Table {assigned_table} reserved successfully!',
        'customer': customer_info
    }

def get_reservations(email=None, time_slot=None):
    query = db.session.query(Reservation).join(Customer)

    # Apply filters if provided
    if email:
        query = query.filter(Customer.customer_email == email)
    if time_slot:
        query = query.filter(Reservation.time_slot == time_slot)

    reservations = query.all()

    results = []
    for r in reservations:
        formatted_time = r.time_slot.strftime('%B %d, %Y %I:%M %p')  # e.g., October 27, 2025 03:00 PM
        results.append({
            'reservation_id': r.reservation_id,
            'customer_name': r.customer.customer_name,
            'customer_email': r.customer.customer_email,
            'table_number': r.table_number,
            'time_slot': formatted_time,
        })

    return {
        'success': True,
        'count': len(results),
        'reservations': results
    }