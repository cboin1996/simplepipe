import datetime

def get_time_now(fmt: str) -> str:
    """Helper method for returning a formatted str timestamp for the current time and date.
    Args:
        fmt (str): the format of the date time str
    Returns: the formatted datetime string
    """
    return datetime.datetime.now().strftime(fmt)