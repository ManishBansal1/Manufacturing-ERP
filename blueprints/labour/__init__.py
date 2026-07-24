from flask import Blueprint

labour_bp = Blueprint(
    "labour",
    __name__,
    url_prefix="/labour"
)

from . import routes