from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send, emit
from twilio.twiml.messaging_response import MessagingResponse
from flask_cors import CORS

app = Flask(__name__)
app.config['FromAPI'] = 'FromAPI'
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/", methods=["GET", "POST", "PUT"])
def sms_reply():
    msg = request.form.get('Body')
    #resp = MessagingResponse()
    #resp.message("hahah")
    outbound_msg = {"senderId": "Charlie", "text": msg}
    print(outbound_msg)
    socketio.emit("FromAPI", jsonify(outbound_msg))
    return jsonify(msg)

if __name__ == '__main__':
    socketio.run(app)
