from flask import flash, Blueprint, request, render_template, redirect, url_for
from chat_app.forms import SignupForm, LoginForm, NewRoomForm
from chat_app import db
from flask_bcrypt import Bcrypt
from chat_app import app
from chat_app.models import User, Room, Message
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO, emit, send, join_room, leave_room



main = Blueprint('main', __name__)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'
    
socketio = SocketIO(app)

@socketio.on('join')
def join(data):
    join_room(data['room_id'])

@socketio.on('message')
def message(message):
    emit('message', message, broadcast=True, room=message['room_id'])
    message = Message(text=message['message'], sender_id=message['sender_id'], room_id=message['room_id'])
    db.session.add(message)
    db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.chat'))
    
    return render_template('index.html')

@main.route('/chat/new', methods=['GET', 'POST'])
@login_required 
def new_room():
    form = NewRoomForm()

    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        new_room = Room(name=form.name.data, creator=[user], members=[user])
        db.session.add(new_room)
        db.session.commit()
        return redirect(url_for('main.room', room_id=new_room.id))
    
    return render_template('new_room.html', form=form)

@main.route('/chat', methods=['GET'])
@login_required
def chat():
    rooms = User.query.filter_by(username=current_user.username).first().rooms
    
    return render_template('chat.html', rooms=rooms)

@main.route('/chat/<room_id>', methods=['GET'])
@login_required
def room(room_id):
    room = Room.query.filter_by(id=room_id).first()
    rooms = User.query.filter_by(username=current_user.username).first().rooms
    messages = Message.query.filter_by(room_id=room_id).all()
    if room:
        if current_user in room.members:
          return render_template('room.html', current_room=room, rooms=rooms, messages=messages, userid=current_user.id)
        else:
          return redirect(url_for('main.chat'))
    else:
        return redirect(url_for('main.chat'))


@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.chat'))
      
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            print(user.password)
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('main.chat'))
            else:
                flash('Incorrect username/password.', 'error')
        else: 
            flash('Incorrect username/password.', 'error')
            
    return render_template('login.html', form=form)


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        new_user = User(name=form.name.data, username=form.username.data, password=hashed_pass)
        
        #Join user to general room with room id 1
        general_room = Room.query.filter_by(id=1).first()
        new_user.rooms.append(general_room)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.login'))
    
    return render_template('signup.html', form=form)
