from wtforms import (
    DateTimeField,
    FloatField,
    TimeField,
    IntegerField,
    SelectField,
)
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

from datetime import time, datetime


class ConfigForm(FlaskForm):
    day_h_sp = FloatField("Day High Set Point", validators=[DataRequired()])
    day_l_sp = FloatField("Day Low Set Point", validators=[DataRequired()])
    night_h_sp = FloatField("Night High Set Point", validators=[DataRequired()])
    night_l_sp = FloatField("Night Low Set Point", validators=[DataRequired()])
    lights_on_time = TimeField("Day Lights On Time", validators=[DataRequired()])
    lights_off_time = TimeField("Day Lights Off Time", validators=[DataRequired()])
    humidity_high_sp = FloatField(
        "Humidity High Set Point", validators=[DataRequired()]
    )
    humidity_low_sp = FloatField("Humidity Low Set Point", validators=[DataRequired()])
    created = DateTimeField("Config Created")

    def populate_form(self, data):
        for name, value in data.items():
            try:
                field = self[name]
            except KeyError:
                continue
            if isinstance(value, str):
                try:
                    value = time.fromisoformat(value)
                except ValueError:
                    try:
                        value = datetime.fromisoformat(value)
                    except ValueError:
                        continue
            field.data = value
        return self


class ReadingForm(FlaskForm):
    unit = SelectField(
        "Unit of Time",
        choices=[("minutes", "Minutes"), ("hours", "Hours"), ("days", "Days")],
    )
    time = IntegerField("Time Period")
