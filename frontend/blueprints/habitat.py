from flask import Blueprint, render_template

from datetime import datetime

from .utils import APITools
from . import utils

bp = Blueprint("habitat", __name__, url_prefix="/habitat")
api_tools = APITools()


@bp.route("/")
def home():
    context = {"page": "habitat"}
    return render_template("habitat.html", **context)


@bp.route("/readings/")
def readings():
    readings = api_tools.find_reading_by_period(unit="hours", time=5)
    readings = [[utils.pretty_datetime(r["time"]), r["temp"]] for r in readings]

    context = {
        "page": "habitat",
        "readings": readings,
    }
    return render_template("readings.html", **context)


@bp.route("/config/")
def config():
    context = {"page": "habitat"}
    return render_template("config.html", **context)
