from flask import Blueprint

worker_blueprint = Blueprint('worker', __name__, template_folder="templates")

from . import controller
