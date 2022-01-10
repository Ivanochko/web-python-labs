from flask import Blueprint

ekz_blueprint = Blueprint('exam_api', __name__)

from . import workers
