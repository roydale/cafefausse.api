from flask import Blueprint, request, jsonify
from datetime import datetime, UTC
from app.services.reservation_service import create_reservation, get_reservations
from app.utils.date_utils import parse_time_slot

reservation_bp = Blueprint('reservation_bp', __name__, url_prefix='reservations')

@reservation_bp.route('', methods=['POST'])
def create_reservation_route():
    data = request.get_json()

    try:
        customer_data = {
            'customer_name': data['customer_name'],
            'customer_email': data['customer_email'],
            'phone_number': data.get('phone_number'),
            'newsletter_signup': data.get('newsletter_signup', False),
        }

        # Parse ISO timestamp into a datetime object
        time_slot = parse_time_slot(data['time_slot'])

        result = create_reservation(customer_data, time_slot)
        return jsonify(result), 201 if result['success'] else 400

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@reservation_bp.route('', methods=['GET'])
def get_reservations_route():
    '''
    Optional query parameters:
      - email (str): filter by customer email
      - time_slot (str): filter by date/time (e.g., "10/27/2025 3:00 PM")
    Example: /api/reservations?email=test@gmail.com&time_slot=10/27/2025 3:00 PM
    '''
    try:
        email = request.args.get('email')
        time_slot = parse_time_slot(request.args.get('time_slot'))

        result = get_reservations(email=email, time_slot=time_slot)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500