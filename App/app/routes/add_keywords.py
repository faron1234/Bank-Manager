from flask import Blueprint, jsonify, request
from ..models import bank_accounts_list

bp = Blueprint('add_keywords', __name__)


# Flask route for adding keywords to a category
@bp.route('/add_keywords', methods=['POST'])
def add_keywords():
    data = request.json
    account_name = data.get('account')
    category_name = data.get('category')
    keywords = data.get('keywords').split(',')

    account = bank_accounts_list.get_account(account_name)
    if not account:
        #logging.error(f"Account not found: {account_name}")
        return jsonify({"error": "Account not found"}), 404

    category = account.get_category(category_name)
    if not category:
        #logging.error(f"Category not found: {category_name}")
        return jsonify({"error": "Category not found"}), 404

    category.addTransactions(account.transactions.getSubset(keywords))
    #logging.debug(f"Keywords added to category {category_name}: {keywords}")

    return jsonify({"message": "Keywords added", "keywords": keywords})
