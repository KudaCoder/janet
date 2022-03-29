from flask_wtf import FlaskForm
from wtforms import DateTimeField, FloatField, TimeField
from wtforms.validators import DataRequired

from datetime import datetime, time


class ConfigForm(FlaskForm):
    day_h_sp = FloatField("Day High Set Point", validators=[DataRequired()])
    day_l_sp = FloatField("Day Low Set Point", validators=[DataRequired()])
    night_h_sp = FloatField("Night High Set Point", validators=[DataRequired()])
    night_l_sp = FloatField("Night Low Set Point", validators=[DataRequired()])
    lights_on_time = TimeField("Day Lights On Time", validators=[DataRequired()])
    lights_off_time = TimeField("Day Lights Off Time", validators=[DataRequired()])
    created = DateTimeField("Config Created Date")

    def populate_form(self, data):
        for name, value in data.items():
            try:
                field = self[name]
            except KeyError:
                continue
            if isinstance(value, str):
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    try:
                        value = time.fromisoformat(value)
                    except ValueError:
                        continue
            field.data = value
        return self
