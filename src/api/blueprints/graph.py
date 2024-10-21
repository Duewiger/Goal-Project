from flask import Blueprint, jsonify
from src.database.database import get_db

bp = Blueprint("graph", __name__, url_prefix="/graph")

@bp.route("/goal_progress/<string:goal_id>")
def goal_progress(goal_id):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT modified_date, rating, assessment 
            FROM goal_history 
            WHERE goal_id = %s 
            ORDER BY modified_date ASC
            """, 
            (goal_id,)
        )
        history = cursor.fetchall()

    data = [
        {
            "date": entry["modified_date"].strftime("%Y-%m-%d %H:%M:%S"),
            "rating": entry["rating"],
            "assessment": entry["assessment"]
        } 
        for entry in history
    ]
    return jsonify(data)

@bp.route("/goal_average_score")
def goal_average_score():
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT DATE(modified_date) as date, AVG(rating) as avg_rating 
            FROM goal_history 
            GROUP BY DATE(modified_date)
            ORDER BY date ASC
            """
        )
        scores = cursor.fetchall()

    data = [
        {
            "date": entry["date"].strftime("%Y-%m-%d"),
            "avg_rating": entry["avg_rating"]
        } 
        for entry in scores
    ]
    return jsonify(data)