from datetime import datetime, UTC

def parse_time_slot(time_slot_str):
    '''
    Converts a human-friendly or ISO date/time string into a UTC datetime object.
    Supports formats like:
      - '10/27/2025 3:00 PM'
      - '2025-10-27T15:00:00Z' (ISO)
    '''
    if not time_slot_str:
        return None

    try:
        # Try U.S. human-friendly format
        return datetime.strptime(time_slot_str, '%m/%d/%Y %I:%M %p').astimezone(UTC)
    except ValueError:
        try:
            # Try ISO format fallback
            return datetime.fromisoformat(time_slot_str).astimezone(UTC)
        except ValueError:
            raise ValueError(f'Invalid time format: {time_slot_str}')
