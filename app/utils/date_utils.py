from datetime import datetime, UTC

def parse_time_slot(time_slot_str, to_utc=True):
    '''
    Converts a human-friendly or ISO date/time string into a datetime object.
    Supports formats like:
      - '10/27/2025 3:00 PM'
      - '2025-10-27T15:00:00Z' (ISO)

    Parameters:
        time_slot_str (str): Input date/time string.
        to_utc (bool): If True (default), converts to UTC time.
                       If False, keeps local time unchanged.
    '''
    if not time_slot_str:
        return None

    naive_datetime = None

    try:
        # Try U.S. human-friendly format
        naive_datetime = datetime.strptime(time_slot_str, '%m/%d/%Y %I:%M %p')
    except ValueError:
        try:
            # Try ISO format fallback
            naive_datetime = datetime.fromisoformat(time_slot_str.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError(f'Invalid time format: {time_slot_str}')

    # Attach local timezone awareness (based on system time zone)
    local_datetime = naive_datetime.replace(tzinfo=datetime.now().astimezone().tzinfo)

    # Convert to UTC by default
    if to_utc:
        return local_datetime.astimezone(UTC)

    return local_datetime