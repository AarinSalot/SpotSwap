from datetime import datetime

def is_time_slot_available(availability, date, start_time, end_time):
    # start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
    # end_datetime = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")
    for avail in availability:
        print(type(avail.date), avail.start_time, avail.end_time, type(date))
        if date == str(avail.date):
            print("Hey I got the date right")
            # Check if the requested time slot overlaps with the availability
            s_time = datetime.strptime(start_time, "%H:%M").time()
            e_time = datetime.strptime(end_time, "%H:%M").time()
            if s_time >= avail.start_time and e_time <= avail.end_time:
                return True 
    return False


def time_slot_id(availability, date, start_time, end_time):
    # start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
    # end_datetime = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")
    for avail in availability:
        print(type(avail.date), avail.start_time, avail.end_time, type(date))
        if date == str(avail.date):
            print("Hey I got the date right")
            # Check if the requested time slot overlaps with the availability
            s_time = datetime.strptime(start_time, "%H:%M").time()
            e_time = datetime.strptime(end_time, "%H:%M").time()
            if s_time >= avail.start_time and e_time <= avail.end_time:
                return avail
    return False