...


def pretty_dt(value):
    if value is not None:
        day = value.day
        return value.strftime("{D} %B, %Y @ %H:%M").replace(
            "{D}", str(day) + ordinal_suffix(day)
        )

    return


def ordinal_suffix(number):
    if number % 10 == 1 and number != 11:
        return "st"
    elif number % 10 == 2 and number != 12:
        return "nd"
    elif number % 10 == 3 and number != 13:
        return "rd"
    else:
        return "th"


def init_app(app):
    app.jinja_env.filters["pretty_dt"] = pretty_dt
