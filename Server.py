#! /usr/bin/env python3

import socket, sqlite3 as lite
from multiprocessing import Process

class IP_To_Name_Control(object):

	def __init__(self):
		global con, cur, data
		con = lite.connect('itnc.db')
		cur = con.cursor()
		cur.execute("DROP TABLE CONTROL;")
		cur.execute("CREATE TABLE CONTROL (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, ip text);")
		con.commit()
		data = []

	def lookup(self, name, typ=None):
		cur.execute("SELECT name, ip FROM CONTROL;")
		rows = cur.fetchall()
		for i in rows:
			data.append(i[0])
			data.append(i[1])

		if typ == 'ip':
			for x in iter(data):
				if x == name:
					try:
						i_p = data[data.index(x) + 1]
						return i_p
					except IndexError: pass

		if typ == 'user':
			for x in iter(data):
				if x == name:
					num = data.index(x) - 1
					return data[num]

	def add(self, name, ip):
		print("ADDING: ", "NAME -->", name, "IP -->", ip)
		cur.execute("INSERT INTO CONTROL(name, ip) values(?, ?);", (name, ip))
		con.commit()

class Chat_Server(object):

	def __init__(self):
		global s, itnc, Name_And_IP
		Name_And_IP = {}
		itnc = IP_To_Name_Control()
		host = '192.168.1.115'
		port = 8090
		s = socket.socket()
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((host, port))
		s.listen(5)

	def _connection_handler(self):
		sock, addr = s.accept()
		if sock and addr:
			p = Process(target=self._chat_handler, args=(addr, sock))
			p.start()
			p.join()

	def _recv_data(self, sock):
		return sock.recv(9999).decode('utf-8')

	def _construct_headers(self, MSGFROM, MSG):
		header = []
		header.append("MSGFROM: "+ MSGFROM + "\n\r")
		header.append("MSG: " + MSG)
		return ''.join(header)

	def _send_data(self, ip, data):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((ip, 9090))
		sock.send(data.encode('utf-8'))

	def _parse_msg(self, msg, ip):
		new_msg = []
		msg_data = msg.splitlines()
		for header in msg_data:
			if 'MSGTO: ' in header:
				msgto = header.replace("MSGTO: ", '')
			if 'MSG: ' in header:
				old_msg = header.replace("MSG: ", '')
		msgtoip = itnc.lookup(msgto, typ='ip')
		msgfrom = itnc.lookup(ip, typ='user')

		new_msg = [msgfrom, "\n\r", old_msg]
		return new_msg, msgtoip

	def _chat_handler(self, addr, sock):
		print("Connection From -->", addr)
		print("Connection Sock -->", sock)
		sock.send("Login".encode('utf-8'))
		print("Sent Login Message")
		login_name = self._recv_data(sock)
		print("Recvied Login Name For", addr[0], "It is", login_name)
		#Code for login valadation
		print("Adding to database")
		itnc.add(login_name, addr[0])
		print("Added to Database")
		sock.send("Ready For Message".encode('utf-8'))
		msg = self._recv_data(sock)
		print("Closing Socket")
		sock.close()
		print("Socket Closed Succesfully")
		print("Recived Message")
		msg_with_headers, mstoip = self._parse_msg(msg, addr[0])
		print("Succesfully Parsed Message")
		print(msg_with_headers, "-->" ,mstoip)
		self._send_data(mstoip, ''.join(msg_with_headers))
		print("Sent Message")

if __name__ == '__main__':
	c = Chat_Server()
	while True:
		c._connection_handler()