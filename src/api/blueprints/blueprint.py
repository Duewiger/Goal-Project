from flask import Blueprint, render_template

from src.util.log_util import log_print

bp = Blueprint("main", __name__, url_prefix="/")

@bp.route("/")
def index():
    log_print("Startseite aufgerufen")
    return render_template("index.html.j2", title="Overview")