from flask_wtf import FlaskForm
from wtforms import DateTimeField, FloatField, TimeField
from wtforms.validators import DataRequired


class ConfigForm(FlaskForm):
    day_h_sp = FloatField("Day High Set Point", validators=[DataRequired()])
    day_l_sp = FloatField("Day Low Set Point", validators=[DataRequired()])
    night_h_sp = FloatField("Night High Set Point", validators=[DataRequired()])
    night_l_sp = FloatField("Night Low Set Point", validators=[DataRequired()])
    lights_on_time = TimeField("Day Lights On Time", validators=[DataRequired()])
    lights_off_time = TimeField("Day Lights Off Time", validators=[DataRequired()])
    created = DateTimeField("Config Created Date")
