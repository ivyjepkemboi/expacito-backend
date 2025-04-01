from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_bcrypt import Bcrypt  # Added bcrypt explicitly
from config import Config
from db import db
from routes.auth_routes import auth_routes
from routes.transaction_routes import transaction_bp  # renamed for consistency
from sqlalchemy import text

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Flask Extensions
db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)  # Initialize bcrypt explicitly
migrate = Migrate(app, db)
CORS(app)  # Enable CORS for all routes

# Expose bcrypt through Flask's extensions explicitly
app.extensions['bcrypt'] = bcrypt  # <-- Important!

# Register Blueprints
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(transaction_bp, url_prefix='/api')

with app.app_context():
    from flask_migrate import upgrade
    upgrade()

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/db-check")
def db_check():
    try:
        result = db.session.execute(text("SELECT 1")).scalar()
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500