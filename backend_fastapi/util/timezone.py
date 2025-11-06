import os
from datetime import datetime
import pytz
from markupsafe import Markup

# --- 1. Read the target timezone from an environment variable ---
# Fallback to 'Asia/Bangkok' (UTC+7) if not set.
# You can change this default to whatever you like.
TARGET_TIMEZONE_STR = os.getenv("DISPLAY_TIMEZONE", "Asia/Bangkok")
try:
    TARGET_TIMEZONE = pytz.timezone(TARGET_TIMEZONE_STR)
except pytz.UnknownTimeZoneError:
    print(f"WARNING: Unknown timezone '{TARGET_TIMEZONE_STR}'. Falling back to UTC.")
    TARGET_TIMEZONE = pytz.utc

# --- 2. Create the reusable formatter function ---
def format_datetime_as_local(model, attribute_name: str) -> Markup:
    """
    A reusable formatter for SQLAdmin that converts a UTC datetime
    from the database to the local timezone defined by DISPLAY_TIMEZONE.
    
    Usage:
    column_formatters = {
        "my_date_column": lambda m, _: format_datetime_as_local(m, "my_date_column")
    }
    """
    # Get the datetime object from the model instance
    utc_datetime = getattr(model, attribute_name, None)

    if not isinstance(utc_datetime, datetime):
        return "" # Return empty if the value is None or not a datetime

    # 1. Make the naive datetime "aware" that it's in UTC
    utc_datetime = utc_datetime.replace(tzinfo=pytz.utc)
    
    # 2. Convert it to the target timezone
    local_datetime = utc_datetime.astimezone(TARGET_TIMEZONE)
    
    # 3. Format it into a nice, human-readable string
    formatted_string = local_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    # 4. Return it as Markup
    return Markup(formatted_string)