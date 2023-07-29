from datetime import date

def calculate_age(date):
    today = date.today()
    return today.year - date.year - ((today.month, today.day) < (date.month, date.day))

    
