from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# Shared Flask extensions for app, models, and routes

db = SQLAlchemy()
mail = Mail()
