from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, send, emit
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from flask_cors import CORS
from api_keys import *
import sqlite3

app = Flask(__name__)
app.config['FromAPI'] = 'FromAPI'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

@app.route('/send', methods=['POST'])
def send():
    #Interpret Input Json
    content = request.get_json()
    var_msg = content.get('text')
    senderId = content.get('senderId')
    ReceiverId = "Cliente"


    #Call Twilio API
    var_celnum_to = 'whatsapp:+5218113934066'
    var_celnum_from = 'whatsapp:+14155238886'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
                              body=var_msg,
                              from_=var_celnum_from,
                              to=var_celnum_to
                          )
    print(message.sid)

    #Save in DB
    conn = sqlite3.connect('msgsdb.sqlite')
    cur = conn.cursor()
    cur.execute('''INSERT INTO Messages (senderCel, senderId, text, ReceiverCel, ReceiverId, messageSid)
                VALUES (?, ?, ?, ?, ?, ?)''', (var_celnum_to, senderId, var_msg, var_celnum_from, ReceiverId, message.sid ))
    conn.commit()

    #Return to Client
    print(content)
    return jsonify(content)


@app.route('/getmsgs', methods=['GET'])
def getmsgs():
    #Get Conversation from DB
    conn = sqlite3.connect('msgsdb.sqlite')
    cur = conn.cursor()
    initial_conver = []
    for row in cur.execute('SELECT * FROM Messages'):
        initial_conver.append({"messageId": row[5], "senderId" : row[1], "text": row[2]})
    return jsonify(initial_conver)

#####AGREGADO
@app.route("/", methods=["POST"])
def sms_reply():
    var_msg = request.form.get('Body')
    var_celnum_to = request.form.get('To')
    var_celnum_from = request.form.get('From')
    senderId = "Cliente"
    ReceiverId = "Agente"
    messageid = request.form.get('MessageSid')

    #Save in DB
    conn = sqlite3.connect('msgsdb.sqlite')
    cur = conn.cursor()
    cur.execute('''INSERT INTO Messages (senderCel, senderId, text, ReceiverCel, ReceiverId, messageSid)
                VALUES (?, ?, ?, ?, ?, ?)''', (var_celnum_to, senderId, var_msg, var_celnum_from, ReceiverId, messageid ))
    conn.commit()
    #resp = MessagingResponse()
    #resp.message("hahah")
    outbound_msg = {"messageId": messageid, "senderId": "Cliente", "text": var_msg}
    print(outbound_msg)
    socketio.emit("FromAPI", outbound_msg)
    return jsonify(var_msg)

if __name__ == '__main__':
    socketio.run(app)
#####AGREGADO

#if __name__ == "__main__":
#    app.run()
