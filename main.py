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
    print('user' + ' has entered the room.'+str(room))
  


@socketio.on('play')
def play(data):
    room = data['channel']
    time=data['time']
    print(str(room)+str(time)+'PLAY REQUEST RECIEVED')
    emit('play',{'time':time},room=room,broadcast=True)
@socketio.on('pause')
def pause(data):
    room = data['channel']
    time=data['time']
    print(str(room)+str(time)+'PAUSE REQUEST RECIEVED')
    emit('pause',{'time':time},room=room,broadcast=True)


@socketio.on('brain')
def on_join(data):
    room = data['channel']
    join_room(room)
    print('user' + ' has entered the room.'+str(room))

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)

@app.route('/<int:roomID>')
def index(roomID):
	return render_template('index.html',roomID=roomID)

if __name__ == '__main__':
	socketio.run(app)
