from flask import Flask


def create_app():
    app = Flask(__name__, template_folder='templates')

    # Import and register the Blueprint
    from .src.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # Register template filters
    @app.template_filter('currency')
    def currency_filter(value):
        return f"£{value:,.2f}"

    @app.template_filter('abs')
    def abs_filter(value):
        return abs(value)

    return app
