import socket, sys, multiprocessing

class Chat_Client(object):

	def __init__(self):
		global s, host
		host = '192.168.1.115'
		port = 8090
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host, port))

	def _login(self):
		self.send(sys.argv[1])

	def send(self, msg):
		s.send(msg.encode('utf-8'))

	def _recive_responce_connection_handler(self):
		so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		so.bind(('', 9090))
		so.listen(5)
		while True:
			sock, addr = so.accept()
			if sock and addr:
				p = multiprocessing.Process(target=self._recive_responce, args=(sock, addr))
				p.start()
	
	def _recive_responce(self, sock, addr):
		rsp = sock.recv(9999)
		if len(rsp) > 1:
			with open("Inbox", 'a') as file:
				file.write(rsp.decode('utf-8'))
				file.close()
				print(rsp.decode('utf-8'))
			sock.close()

	def _start_responce_process(self):
		p = multiprocessing.Process(target=self._recive_responce_connection_handler)
		p.start()

	def _request_msg(self):
		to = input("TO:>>> ")
		data = input("MSG:>>> ")
		self.send("MSGTO: "+to+ "\r\n"+ "MSG: "+data)

	def _chat_handler(self):
		login = s.recv(1024)
		if login.decode('utf-8') is 'Login':
			print("Login Request...")
		print("Attempting Login...")
		self._login()
		self._start_responce_process()
		msg_r = s.recv(1024)
		if msg_r.decode('utf-8') == 'Ready For Message':
			print("Server Ready For Msg...")
			self._request_msg()

if __name__ == '__main__':
	c = Chat_Client()
	c._chat_handler()