from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get('DATABASE_URL') or 'sqlite:///chatapp.db'
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)

app.app_context().push()
from chat_app.routes import main

app.register_blueprint(main)

with app.app_context():
    db.create_all()

