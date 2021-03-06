from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send, join_room, leave_room,emit
from flask_cors import CORS
import os, json, boto3, threading, s3transfer, sys
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY']=os.getenv("SECRET_KEY")
socketio=SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")
client = boto3.client('sts')


@socketio.on('message')
def handleMessage(msg):
	print ('Message: '+msg)
	send (msg,broadcast=True)

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

@app.route('/room/<string:roomID>')
def roomN(roomID):
    response = client.assume_role(RoleArn='arn:aws:iam::670717215081:role/watchsyncROLE', RoleSessionName='watchsyncSession')
    return render_template('roomN.html',roomID=roomID,AccessKeyId=response.get('Credentials').get('AccessKeyId'),SecretAccessKey=response.get('Credentials').get('SecretAccessKey'),SessionToken=response.get('Credentials').get('SessionToken'))
@app.route('/create',methods=['POST', 'GET'])
def create():
    response = client.assume_role(RoleArn='arn:aws:iam::670717215081:role/watchsyncROLE', RoleSessionName='watchsyncSession')
    return render_template('create.html',AccessKeyId=response.get('Credentials').get('AccessKeyId'),SecretAccessKey=response.get('Credentials').get('SecretAccessKey'),SessionToken=response.get('Credentials').get('SessionToken'))

@app.route('/join')
def join():
	return render_template('join.html')
if __name__ == '__main__':
	socketio.run(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    s3=boto3.client('s3')
    file=request.files['myfile']
    file.seek(0,os.SEEK_END)
    file_length=file.tell()
    sys.stdout.write('stdout')
    print('print')
    class ProgressPercentage(object):
        def __init__(self, filename,filesize):
            self._filename = filename
            self._size = filesize
            self._seen_so_far = 0
            self._lock = threading.Lock()

        def __call__(self, bytes_amount):
            with self._lock:
                self._seen_so_far += bytes_amount
                percentage = (self._seen_so_far / self._size) * 100
                sys.stdout.write(
                    "\r%s  %s / %s  (%.2f%%)" % (
                        self._filename, self._seen_so_far, self._size,
                        percentage))

    s3.upload_fileobj(
    file, 'watchsyncus', 'newfile.mp4',
    Callback=ProgressPercentage(file,file_length)
    )   
    return('<h1>FILE UPLOADED<h1>')



if __name__ == '__main__':
    app.run(debug=True)
