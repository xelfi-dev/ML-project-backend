from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://transactions_k7us_user:8clpBdSCNtfjzzEcGk67FsyONA1TwelP@dpg-ct8tu8btq21c739uogkg-a.oregon-postgres.render.com/transactions_k7us'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, disables modification tracking

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
