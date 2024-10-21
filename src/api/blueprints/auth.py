from flask import (
    Blueprint, g, flash, redirect, render_template, request, session, url_for
)
import uuid
from werkzeug.security import check_password_hash, generate_password_hash
from src.database.database import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                user_id = str(uuid.uuid4())
                with db.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO users (id, username, password) VALUES (%s, %s, %s)",
                        (user_id, username, generate_password_hash(password)),
                    )
                    db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html.j2")

@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE username = %s", (username,)
            )
            user = cursor.fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("main.index"))

        flash(error)

    return render_template("auth/login.html.j2")

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.logout_success"))

@bp.route("/logout_success")
def logout_success():
    return render_template("auth/logout_success.html.j2")

@bp.before_app_request
def load_logged_in_user():
    """Loads the user if logged in."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            g.user = cursor.fetchone()