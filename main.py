from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder="static", template_folder="templates")
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('client_data')
def receive_data(data):
    # Broadcast the data to all connected clients
    emit('server_data', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8090, use_reloader=True)
