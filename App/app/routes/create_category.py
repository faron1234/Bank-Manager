from flask import Blueprint, request, jsonify
from ..models import bank_accounts_list, Category

bp = Blueprint('create_category', __name__)


# Flask route for creating a new category
@bp.route('/create_category', methods=['POST'])
def create_category():
    data = request.get_json()
    account_name = data.get('account')
    category_name = data.get('category')

    account = bank_accounts_list.get_account(account_name)
    if not account:
        # logging.error(f"Account not found: {account_name}")
        return jsonify({"error": "Account not found"}), 404

    newCategory = Category(category_name)
    account.addCategory(newCategory)
    # logging.debug(f"Category created: {category_name} in account {account_name}")

    return jsonify({"message": "Category created", "category": category_name})
