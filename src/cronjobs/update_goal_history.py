from src.database.database import get_db

def check_for_updates():
    """Checks for new entries in the `goal_history` table and processes them."""
    db = get_db()
    with db.cursor() as cursor:
        # Find entries that were modified recently
        cursor.execute("""
            SELECT gh.* 
            FROM goal_history gh 
            JOIN notifications n ON n.table_name = 'goal_history' 
            WHERE n.processed = 0 AND gh.modified_date > NOW() - INTERVAL 1 MINUTE
        """)
        updates = cursor.fetchall()

    if updates:
        print(f"{len(updates)} Änderungen in der Ziel-Historie gefunden.")

        for update in updates:
            print(f"Verarbeite Änderung: Ziel ID {update['goal_id']}, Bewertung {update['rating']}, Kommentar {update['assessment']}")

        # Mark the processed notifications
        with db.cursor() as cursor:
            cursor.execute("UPDATE notifications SET processed = 1 WHERE table_name = 'goal_history'")
        db.commit()
    else:
        print("Keine neuen Änderungen in der Ziel-Historie gefunden.")

if __name__ == "__main__":
    check_for_updates()