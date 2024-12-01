from flask import Flask
from models import db
from routes.repo_routes import repo_bp
from routes.issue_routes import issue_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bithub.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(repo_bp)
    app.register_blueprint(issue_bp)

    return app

# if __name__ == '__main__':
#     app = create_app()
#     with app.app_context():
#         db.create_all()
#     print("Database ready")
#     app.run(debug=True)

