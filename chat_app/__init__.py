from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatap.db'
app.config['SECRET_KEY'] = 'secretkey'

db = SQLAlchemy(app)

from chat_app.routes import main

app.register_blueprint(main)

with app.app_context():
    db.create_all()

