from flask import Blueprint, render_template
from ..models import bank_accounts_list

bp = Blueprint('index', __name__)


# Flask route for displaying index.html page (home)
@bp.route('/')
def index():
    return render_template('index.html', accounts=bank_accounts_list.all_accounts(), banks=bank_accounts_list.banks())
