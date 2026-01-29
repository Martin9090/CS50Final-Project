import datetime

from flask import redirect, render_template, session
from functools import wraps
from datetime import date


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def calculate_age(dob):
    """Looking to show age as year from date on index page."""
    born = datetime.datetime.strptime(dob, "%Y-%m-%d").date()
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def datetime_change(date):
    """Changing the format of how date time is displayed"""
    date_format = "%Y-%m-%dT%H:%M"
    time_taken = datetime.datetime.strptime(date, date_format)
    return time_taken.strftime("%d/%b %H:%M")


def time():
    return datetime.datetime.now()
