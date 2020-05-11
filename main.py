from flask import Flask,render_template
from flask_socketio import SocketIO, send, join_room, leave_room,emit
app = Flask(__name__)
app.config['SECRET_KEY']='mysecret'
socketio=SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

@socketio.on('message')
def handleMessage(msg):
	print ('Message: '+msg)
	send (msg,broadcast=True)

@socketio.on('jumba')
def handleJumba(data):
	print('hi')
	emit('WE ARE IN ROOMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM: '+str(data['channel']),room=data['channel'])

@socketio.on('join')
def on_join(data):
    room = data['channel']
    join_room(room)
    emit('giveMeTime',{'channel':room},room=room,broadcast=True,include_self=False)
    print('user' + ' has entered the room.'+str(room))


@socketio.on('syncWithTime')
def syncTime(data):
	room=data['channel']
	time=data['time']
	emit('syncWithTime',{'time':time,'paused':data['paused']},room=room,broadcast=True,include_self=False)
  
  


@socketio.on('play')
def play(data):
    room = data['channel']
    time=data['time']
    print(str(room)+str(time)+'PLAY REQUEST RECIEVED')
    emit('play',{'time':time},room=room,broadcast=True,include_self=False)
@socketio.on('pause')
def pause(data):
    room = data['channel']
    time=data['time']
    print(str(room)+str(time)+'PAUSE REQUEST RECIEVED')
    emit('pause',{'time':time},room=room,broadcast=True,include_self=False)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)

@app.route('/<int:roomID>')
def roomN(roomID):
	return render_template('roomN.html',roomID=roomID)

@app.route('/')
def index():
	return render_template('index.html')
@app.route('/create')
def create():
	return render_template('create.html')
@app.route('/join')
def join():
	return render_template('join.html')
if __name__ == '__main__':
	socketio.run(app)
