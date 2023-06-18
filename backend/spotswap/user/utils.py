from datetime import datetime

def is_time_slot_available(availability, start_date, start_time, end_date, end_time):
    start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
    end_datetime = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")
    
    # Check if the requested time slot overlaps with the availability
    if start_datetime >= availability.start_datetime and end_datetime <= availability.end_datetime:
        return True
    
    return False