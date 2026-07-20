from flask import Blueprint

jobwork_bp = Blueprint(
    "jobwork",
    __name__,
    url_prefix="/jobwork"
)

from . import routes