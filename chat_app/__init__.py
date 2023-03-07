from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

import os
from flask_migrate import Migrate



app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///chatapp.db'
app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get('DATABASE_URL') or 'sqlite:///chatapp.db'
app.config['SECRET_KEY'] = 'secretkey'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.app_context().push()
from chat_app.routes import main

app.register_blueprint(main)

with app.app_context():
    db.create_all()

