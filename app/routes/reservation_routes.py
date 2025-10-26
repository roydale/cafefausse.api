from flask import Blueprint, request, jsonify
from datetime import datetime, UTC
from app.services.reservation_service import create_reservation

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
        time_slot = datetime.fromisoformat(data['time_slot']).astimezone(UTC)

        result = create_reservation(customer_data, time_slot)
        return jsonify(result), 201 if result['success'] else 400

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
