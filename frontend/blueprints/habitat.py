from flask import Blueprint, render_template, request

import plotly.express as px
import pandas as pd
import plotly

from datetime import datetime, time
import json

from frontend.forms import ConfigForm
from .utils import APITools

bp = Blueprint("habitat", __name__, url_prefix="/habitat")
api_tools = APITools()


@bp.route("/")
def home():
    context = {"page": "habitat"}
    return render_template("habitat.html", **context)


@bp.route("/readings/")
def readings():
    readings = api_tools.find_reading_by_period(unit="minutes", time=10)
    data = {
        "time": [r["time"] for r in readings],
        "temp": [r["temp"] for r in readings],
        "hum": [r["hum"] for r in readings],
    }
    df = pd.DataFrame(data)
    fig = px.line(
        df,
        x="time",
        y=["temp", "hum"],
        title="Habitat Conditions",
    )
    fig = fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(width=1400, height=500)
    habi_graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    context = {
        "page": "habitat",
        "habitat_graph": habi_graph,
    }

    return render_template("readings.html", **context)


@bp.route("/config/", methods=["GET", "POST"])
def config():
    form = ConfigForm(request.form or None)
    if form.validate_on_submit():
        api_tools.set_config(form.data)

    config = api_tools.get_config()
    config["lights_on_time"] = time.fromisoformat(config["lights_on_time"])
    config["lights_off_time"] = time.fromisoformat(config["lights_off_time"])
    config["created"] = datetime.fromisoformat(config["created"])
    form.populate_form(config)

    context = {"page": "habitat", "form": form}
    return render_template("config.html", **context)
