from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from chat_app.models import User, Room

class NewRoomForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=1, max=80)], render_kw={"placeholder": "Room Name"})
    submit = SubmitField('Create Room')

    def validate_room_name(self, room_name):
        existing_room =  Room.query.filter_by(room_name=room_name.data).first()
        if existing_room:
            raise ValidationError('Room name already exists. Please try a different room name.')

class SignupForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=1, max=80)], render_kw={"placeholder": "Name"})
    username = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=1, max=80)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        existing_user =  User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError('Username already exists. Please try a different username.')
        

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=1, max=80)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')