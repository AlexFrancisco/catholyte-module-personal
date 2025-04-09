from flask import Blueprint

personal_bp = Blueprint('personal', __name__, template_folder='templates')

from app.modules.personal import routes