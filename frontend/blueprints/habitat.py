from flask import Blueprint, render_template, request
from flask_login import login_user, login_required

import plotly.express as px
import pandas as pd
import plotly

import json

from frontend.forms import ConfigForm, ReadingForm
from .utils import APITools

bp = Blueprint("habitat", __name__, url_prefix="/habitat")
api_tools = APITools()


@bp.route("/")
def home():
    reading = api_tools.current_reading()

    context = {"page": "habitat", "reading": reading}
    return render_template("habitat.html", **context)


@bp.route("/readings", methods=["GET", "POST"])
def readings():
    habi_graph = None
    form = ReadingForm()
    if form.validate_on_submit():
        data = form.data
        readings = api_tools.find_reading_by_period(
            unit=data["unit"], time=data["time"]
        )
        data = {
            "Time": [r["time"] for r in readings],
            "Temperature": [r["temp"] for r in readings],
            "Humidity": [r["hum"] for r in readings],
        }
        df = pd.DataFrame(data)
        fig = px.line(
            df,
            x="Time",
            y=["Temperature", "Humidity"],
            title="Habitat Conditions",
        )
        fig = fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(
            width=1400,
            height=500,
            paper_bgcolor="rgba(0, 0, 0, 0)",
            plot_bgcolor="rgba(111, 117, 128, .3)",
            title_font_size=25,
            title_font={"family": "Josefin Sans"},
            modebar={"bgcolor": "rgba(236, 236, 236, 1)"},
        )
        habi_graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    context = {
        "page": "habitat",
        "content": "reading",
        "form": form,
        "habitat_graph": habi_graph,
    }
    return render_template("readings.html", **context)


@bp.route("/config", methods=["GET", "POST"])
@login_required
def config():
    form = ConfigForm(request.form or None)
    if form.validate_on_submit():
        api_tools.set_config(form.data)

    config = api_tools.get_config()
    if config is not None:
        form.populate_form(config)

    context = {"page": "habitat", "content": "config", "form": form}
    return render_template("config.html", **context)
