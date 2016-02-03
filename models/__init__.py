import urllib

from flask import current_app
from flask.ext.sqlalchemy import SQLAlchemy

try:
    current_app._get_current_object()
    app = current_app
except RuntimeError as e:
    raise RuntimeError("Please push flask context first !!")
db = SQLAlchemy(app)
