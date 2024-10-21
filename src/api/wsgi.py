""" The script for wsgi server access. """
from src.api.app import create_app
APP = create_app()
