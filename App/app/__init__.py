from flask import Flask


def create_app():
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')

    # Import and register Blueprints here
    from .routes import account, add_keywords, category, create_account, create_category, index, search_transactions

    app.register_blueprint(account.bp)
    app.register_blueprint(add_keywords.bp)
    app.register_blueprint(category.bp)
    app.register_blueprint(create_account.bp)
    app.register_blueprint(create_category.bp)
    app.register_blueprint(index.bp)
    app.register_blueprint(search_transactions.bp)

    # Register template filters
    @app.template_filter('currency')
    def currency_filter(value):
        return f"£{value:,.2f}"

    @app.template_filter('abs')
    def abs_filter(value):
        return abs(value)

    print(f"Template folder: {app.template_folder}")
    print(f"Static folder: {app.static_folder}")

    return app
