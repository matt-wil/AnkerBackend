import re

def validate_phone_number(phone_number):
    regex = r'^[0-9]{11}$'
    if re.fullmatch(regex, phone_number):
        return True
    else:
        return False

def validate_date(date):
    regex = r'^\d{4}-\d{2}-\d{2}$'
    if re.fullmatch(regex, date):
        return True
    else:
        return False

def validate_time(time):
    regex = r'^\d{2}:\d{2}$'
    if re.fullmatch(regex, time):
        return True
    else:
        return False

