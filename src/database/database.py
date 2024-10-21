''' Module for database connection '''

from flask import current_app, g

import click
from pymysql import connect, cursors

from src.util import config_util

def init_db():
    ''' Initializes the database using the schema.sql file. '''
    db = get_db()

    with current_app.open_resource('../database/schema.sql') as f:
        sql_script = f.read().decode('utf-8')
        
        for statement in sql_script.split(';'):
            if statement.strip():
                db.cursor().execute(statement)
        db.commit()

    create_trigger(db)

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    ''' Register the database functions with the Flask app. '''
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def create_trigger(db):
    """Creates the trigger for changes in the goal_history table."""
    trigger_statement = """
    CREATE TRIGGER after_goal_history_insert
    AFTER INSERT ON goal_history
    FOR EACH ROW
    BEGIN
        INSERT INTO notifications (table_name, action) VALUES ('goal_history', 'insert');
    END;
    """
    with db.cursor() as cursor:
        cursor.execute(trigger_statement)
    db.commit()

def get_db():
    ''' Returns the database connection. If it doesn't exist yet, it is created
    first.
    Returns:
        pymysql.connections.Connection -- The database connection. '''
    if 'db' not in g:
        db_config = config_util.get("database")
        g.db = connect(host=db_config["hostname"],
                       user=db_config["username"],
                       password=db_config["password"],
                       db=db_config["database"],
                       cursorclass=cursors.DictCursor)
    return g.db

def close_db(e=None):
    ''' Closes the database connections, if any exist. This is usually called
    after a request is done. '''
    db = g.pop('db', None)
    if db is not None:
        db.close()