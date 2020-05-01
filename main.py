from flask import Flask,render_template
from flask_socketio import SocketIO, send
import redis
r = redis.from_url("redis://h:p1bcee469e3e66d483eac699334a5b69be5bb1f9b493df5727fdbe1c0661f8481@ec2-34-194-242-244.compute-1.amazonaws.com:13149")
app = Flask(__name__)
app.config['SECRET_KEY']='mysecret'
socketio=SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

@socketio.on('message')
def handleMessage(msg):
	print ('Message: '+msg)
	send (msg,broadcast=True)

@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	socketio.run(app)
