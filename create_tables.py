import sqlite3

conn = sqlite3.connect('msgsdb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Messages')

cur.execute('''
CREATE TABLE Messages (senderCel TEXT, senderId TEXT, text TEXT, ReceiverCel TEXT, ReceiverId TEXT, messageSid TEXT)''')
