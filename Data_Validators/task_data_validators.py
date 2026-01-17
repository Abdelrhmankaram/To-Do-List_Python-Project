from datetime import datetime

def validate_due_date(due_date: str, date_format: str = "%d-%m-%Y %H:%M") -> bool:
    """
    Validate that the due date:
    1. Matches the format DD-MM-YYYY HH:MM
    2. Is in the future
    """
    try:
        parsed_date = datetime.strptime(due_date, date_format)
        return parsed_date > datetime.now()
    except ValueError:
        return False
