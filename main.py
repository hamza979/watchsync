from flask import Flask,render_template
from flask_socketio import SocketIO, send
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
