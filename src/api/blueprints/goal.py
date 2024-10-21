from flask import Blueprint, g, render_template, request, redirect, url_for, flash
from src.database.database import get_db
import uuid

bp = Blueprint("goal", __name__, url_prefix="/goal")

@bp.route("/", methods=["GET"])
def index():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM goals")
        goals = cursor.fetchall()

    return render_template("goal/goal_index.html.j2", goals=goals)

@bp.route("/create", methods=("GET", "POST"))
def create():
    if g.user is None:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        department = request.form["department"]
        statement = request.form["statement"]
        criteria = request.form["criteria"]
        rating = request.form["rating"]
        assessment = request.form["assessment"]
        last_modified_by = g.user["id"]

        error = None

        if not department:
            error = "Department is required."
        elif not statement:
            error = "Statement is required."
        elif not criteria:
            error = "Criteria is required."
        elif not rating or not rating.isdigit() or not (1 <= int(rating) <= 10):
            error = "Rating must be a number between 1 and 10."
        elif not assessment:
            error = "Assessment is required."

        if error is not None:
            flash(error)
        else:
            goal_id = str(uuid.uuid4())
            db = get_db()
            try:
                with db.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO goals (id, department, statement, criteria, rating, assessment, last_modified_by)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (goal_id, department, statement, criteria, int(rating), assessment, last_modified_by),
                    )
                    db.commit()

                with db.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO notifications (id, table_name, action) VALUES (%s, %s, %s)",
                        (str(uuid.uuid4()), 'goals', 'create')
                    )

                with db.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO goal_history (id, goal_id, rating, assessment, modified_by) VALUES (%s, %s, %s, %s, %s)",
                        (str(uuid.uuid4()), goal_id, int(rating), assessment, last_modified_by)
                    )

                flash("Goal created successfully.")
                return redirect(url_for("goal.index"))
            except Exception as e:
                flash(f"Error creating goal: {str(e)}")
                db.rollback()

    return render_template("goal/goal_create.html.j2")

@bp.route("/update/<string:goal_id>", methods=("GET", "POST"))
def update(goal_id):
    if g.user is None:
        return redirect(url_for("auth.login"))

    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM goals WHERE id = %s", (goal_id,))
        goal = cursor.fetchone()

    if goal is None:
        flash("Goal not found.")
        return redirect(url_for("goal.index"))

    if request.method == "POST":
        new_data = {
            "department": request.form["department"],
            "statement": request.form["statement"],
            "criteria": request.form["criteria"],
            "rating": request.form["rating"],
            "assessment": request.form["assessment"],
            "last_modified_by": g.user["id"],
        }

        changes = {key: value for key, value in new_data.items() if str(value) != str(goal[key])}

        if not changes:
            flash("No changes detected.")
        else:
            set_clause = ", ".join([f"{key} = %s" for key in changes.keys()])
            values = list(changes.values()) + [goal_id]

            try:
                with db.cursor() as cursor:
                    cursor.execute(
                        f"UPDATE goals SET {set_clause} WHERE id = %s",
                        values
                    )
                    db.commit()

                with db.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO notifications (id, table_name, action) VALUES (%s, %s, %s)",
                        (str(uuid.uuid4()), 'goals', 'update')
                    )

                with db.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO goal_history (id, goal_id, rating, assessment, modified_by) VALUES (%s, %s, %s, %s, %s)",
                        (str(uuid.uuid4()), goal_id, int(new_data["rating"]), new_data["assessment"], g.user["id"])
                    )

                flash("Goal updated successfully.")
                return redirect(url_for("goal.index"))
            except Exception as e:
                flash(f"Error updating goal: {str(e)}")
                db.rollback()

    return render_template("goal/goal_update.html.j2", goal=goal)

@bp.route("/delete/<string:goal_id>", methods=("POST",))
def delete(goal_id):
    if g.user is None:
        return redirect(url_for("auth.login"))

    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM goals WHERE id = %s", (goal_id,))
        goal = cursor.fetchone()

    if goal is None:
        flash("Goal not found.")
    else:
        try:
            with db.cursor() as cursor:
                cursor.execute("DELETE FROM goals WHERE id = %s", (goal_id,))
                db.commit()

                with db.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO notifications (id, table_name, action) VALUES (%s, %s, %s)",
                        (str(uuid.uuid4()), 'goals', 'delete')
                    )

            flash("Goal deleted successfully.")
        except Exception as e:
            flash(f"Error deleting goal: {str(e)}")
            db.rollback()

    return redirect(url_for("goal.index"))

@bp.route("/api/goal_history")
def api_goal_history():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM goal_history")
        goal_history = cursor.fetchall()
    
    return {"goal_history": goal_history}