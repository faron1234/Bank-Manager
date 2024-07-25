from flask import Blueprint, request, jsonify
from ..models import bank_accounts_list

bp = Blueprint('create_account', __name__)


# Flask route for creating a new account
@bp.route('/create_account', methods=['POST'])
def create_account():
    data = request.get_json()
    account_name = data.get('account_name', '').strip()
    bank = data.get('bank', '').strip()

    if not account_name or not bank:
        return jsonify({'error': 'Account name or bank is missing'}), 400

    try:
        bank_accounts_list.add_account(account_name, bank)
    except ValueError as e:
        # logging.error(f"Error creating account: {e}")
        return jsonify({'error': str(e)}), 400

    return jsonify({"message": "Account created", "account": account_name})
