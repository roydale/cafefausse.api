from datetime import datetime, UTC, timedelta
import re
from app.models import Customer, Reservation
from app.extensions import db

def validate_reservation_input(data):
    errors = {}

    # ---------- Validate Full Name ----------
    if not data.get('customer_name'):
        errors['customer_name'] = 'Full name is required.'

    # ---------- Validate Email ----------
    email = data.get('customer_email')
    if not email:
        errors['customer_email'] = 'Email address is required.'
    elif not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        errors['customer_email'] = 'Invalid email address format.'

    # ---------- Validate Phone (optional) ----------
    phone = data.get('phone_number')
    if phone and not re.match(r'^[0-9()+\s-]{7,20}$', phone):
        errors['phone_number'] = 'Invalid phone number format.'

    # ---------- Validate Guest Count ----------
    guest_count = data.get('guest_count')
    if guest_count is None:
        errors['guest_count'] = 'Number of guests is required.'
    elif not isinstance(guest_count, int) or guest_count <= 0:
        errors['guest_count'] = 'Guest count must be a positive integer.'

    # ---------- Validate Date and Time Slot ----------
    time_slot = data.get('time_slot')
    if not time_slot:
        errors['time_slot'] = 'Date and time are required.'
    else:
        try:
            # now = datetime.now(UTC)
            now = datetime.now().astimezone()

            if time_slot < now:
                errors['time_slot'] = 'Reservations cannot be made for past times.'
            else:
                weekday = time_slot.weekday()  # Monday=0, Sunday=6
                hour = time_slot.hour

                # ---------- Sunday (5 PM – 9 PM, last slot 8 PM) ----------
                if weekday == 6:
                    if hour < 17 or hour > 20:
                        errors['time_slot'] = 'Reservation hours on Sundays are 5 to 8 PM.'

                # ---------- Monday–Saturday (5 PM – 11 PM, last slot 10 PM) ----------
                else:
                    if hour < 17 or hour > 22:
                        errors['time_slot'] = 'Reservation hours Mon-Sat are 5 to 10 PM.'

                # ---------- Hourly intervals only ----------
                if time_slot.minute != 0:
                    errors['time_slot'] = 'Reservations are in hourly intervals (e.g., 5 PM, 6 PM).'

                # ---------- Same-day restriction: at least one hour later ----------
                local_now = now.astimezone(time_slot.tzinfo)
                if time_slot.date() == local_now.date():
                    if time_slot <= (local_now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)):
                        errors['time_slot'] = 'Reservations must be at least one hour later than the current time.'
                        
        except ValueError:
            errors['time_slot'] = 'Invalid date or time format.'

    return errors

def create_reservation(customer_data, time_slot, guest_count):
    name = customer_data.get('customer_name')
    email = customer_data.get('customer_email')
    phone = customer_data.get('phone_number')
    
    # Combine into one payload for validation
    validation_data = {
        'customer_name': name,
        'customer_email': email,
        'phone_number': phone,
        'guest_count': guest_count,
        'time_slot': time_slot
    }
    
    # Run validations
    errors = validate_reservation_input(validation_data)
    if errors:
        return {
            'success': False,
            'message': 'Validation failed.',
            'errors': errors,
            'data': {}
        }
    
    # Create or find customer
    customer = Customer.query.filter_by(customer_email=email).first()
    is_new_customer = False
    if not customer:
        customer = Customer(**customer_data)
        db.session.add(customer)
        db.session.commit()
        is_new_customer = True

    # Assign table
    assigned_table = Reservation.assign_random_table(time_slot)
    table_number = 0 if assigned_table is None else assigned_table
    
    reservation_info = {
        'customer_name': customer.customer_name,
        'customer_email': customer.customer_email,
        'reservation_name': name,
        'table_number': table_number,
        'is_new_customer': is_new_customer
    }
    
    if not assigned_table:
        return {
            'success': False, 
            'message': 'Sorry, all tables are full at this time. Please select a different date or time.',
            'errors': {},
            'data': reservation_info
        }

    # Create reservation
    reservation = Reservation(
        customer_id=customer.customer_id,
        time_slot=time_slot.astimezone(UTC),
        table_number=table_number,
        guest_count=guest_count,
        reservation_name=name
    )
    db.session.add(reservation)
    db.session.commit()

    return {
        'success': True, 
        'message': f'Table {assigned_table} reserved successfully!',
        'errors': {},
        'data': reservation_info
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
            'reservation_name': r.reservation_name,
            'customer_name': r.customer.customer_name,
            'customer_email': r.customer.customer_email,
            'table_number': r.table_number,
            'guest_count': r.guest_count,
            'time_slot': formatted_time,
        })

    return {
        'success': True,
        'count': len(results),
        'data': results
    }