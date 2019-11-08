"""
Written By : Tanmay Upadhyay
Email : kevinthemetnik@gmail.com
Facebook : /tanmayupadhyay91

This is client part of Chat-Bot V0.1,

(Chat with Anyone Privately: Secure)

 Converstation between client and server ie.users of this program will be completely encrypted and secured using , No one can access to your private
 conversation unless they have the key, and are tapping your conversation by implementing MITM type attacks.
 Therefore, Keep key safe and only share it with your partner.

 If you are reading this script for learning purpose, then you will learn here,

  >Object Oriented Programming
  >implementation of threading
  >implementation of socket
  >implementation of Cryptographic encryption to encrypt and decrypt messages



"""

from sys import exit
from os import environ #! to get computer name
from time import sleep #!for delay
import socket,threading #! for networking and multithreading
try:
	from cryptography.fernet import Fernet #! for establishing encrypted tunnel.
except ImportError:
	print('Cryptography Module Is Required, Please Use PIP To Install it : pip install cryptography\n')
	input()
class AuthenticateProgram(object):
	"""
	This class will establish a safe mechanism for message sharing between client and server, to avoid MITM and other 
	 Information breach.
	"""
	def __init__(self,securitykeyfile):
		self.securitykeyfile = securitykeyfile
		try:
			#! take key if found stored already.
			with open(self.securitykeyfile,'rb') as key:
				self.security_key=key.read()
				print('Encryption Key Found, Please Ensure Client Have Same %s Key File.'%EstablishConnection.securitykeyfile)

				#!key is generated you need to give the same to your partner.
		except FileNotFoundError:
			#!key deleted or not generated (first time)
			print("Encryption Key Not Found, Generating Now. . . ")
			self.GenerateKey()
	def GenerateKey(self):
		"""
		This method is used to check the presence of key file, if not found then it will generate it  automatically.
		"""
		print('Encryption Key Generated, Send %s to Your Client.'%EstablishProgram.securitykeyfilename)
		#!called when key is not present.
		created_key = Fernet.generate_key() #!for generating random key for our encryption.
		with open(self.securitykeyfile,'wb') as key:
			writekey = key.write(created_key)
			#!key generated successfully.
		with open(self.securitykeyfile,'rb') as key:
			self.security_key=key.read()


	def EncryptMessage(self,message):
		#!this method will encrypt message based on validation key.
		put_key = Fernet(self.security_key)
		encrypted_text=put_key.encrypt(message.encode())
		return encrypted_text
	def DecryptMessage(self,encrypted_message):
		#!This method will decrypt incomming encrypted message.
		put_key = Fernet(self.security_key)
		decrypted_text=put_key.decrypt(encrypted_message)
		decrypted_text = decrypted_text.decode()
		return decrypted_text



class EstablishConnection(threading.Thread,AuthenticateProgram):
	securitykeyfile = 'security.key' #! Dont touch it, if you don't know what it does.
	try:
		mycomputername = "CP:"+environ['COMPUTERNAME'] #! capturing our computer name, to send it to server.
	except KeyError:
		#!raise duing operation on android.
		mycomputername = "CP: Client"
	client_port = 4545 #!port should match the server's port
	server_address = "192.168.1.5" #! on wan connection use external Ip / DNS
	connect_tries = 5

	"""This class with define connection mechanism of our program
	   This program will try to establish a connection to server, if got server online it will try to connect with it
	   Otherwise it will show server is offline or connection refused by server."""
	def __init__(self):
		AuthenticateProgram.__init__(self,EstablishConnection.securitykeyfile)
		threading.Thread.__init__(self)
		self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		banner = """
		[+][-][/][*]
		[-][+][*][/]
		[.][,][?][\]
		[^][#][@][!]
		[&][(][)][-]

		PyTalker-V01 ( Python Program To Share Secured Important Messages Privately.)
		
		Written By : Tanmay Upadhyay
		Email : kevinthemetnik@gmail.com
		Facebook : /tanmayupadhyay91

		[server = Your Chat Partner]

		"""
		print(banner)
		print('(Press Enter To Keep Conversation Going.)')
		print("______________________________________________")

		print("[!] socket created successfully.")
		while True:
			try:
				#! I said to server, please let me in .
				self.sock.connect((EstablishConnection.server_address,EstablishConnection.client_port))
			except ConnectionRefusedError:
				#! may raise if you start client before server.
				print("Unable To Establish Connect To The Server, Trying Again [ SERVER OFFLINE / NO NETWORK ] . . .")
				continue
			print("[SERVER ONLINE] Trying To Establish Secure Connect With Server . . . . ")
			#thread1=threading.Thread(target=self.SendToServer)
			thread2=threading.Thread(target=self.RecvFromServer) #! delegating message receiving function to our child thread which will run concurrently.
			#thread1.start()
			thread2.start()
			while True:
				if self.inital_step == False:
					#wait till the connection is validated.
					continue
				try:
					#!we will handle message sending function in our main thread, and receiving in our children thread.
					self.sendmsg=input("(You) ")
				except KeyboardInterrupt:
					self.sendmsg = ""
					quitcmd=input("[?] Do you really want to end conversation with %s [Y/N] ? "%EstablishConnection.server_address)
					if quitcmd == 'y' or quitcmd == 'Y':
						self.sock.close()
					else:
						pass
				if self.sendmsg == "":
					pass
				else:
					#!passing each string message to our encrytion mechanism.
					self.enc_sendmsg=self.EncryptMessage(self.sendmsg)
					self.sock.sendall(self.enc_sendmsg) #!sending encrypted message only.
					pass

	def RecvFromServer(self):
		self.inital_step = False #! To handle some initial formalities.
		self.send_mycomputername = self.sock.sendall(self.EncryptMessage(EstablishConnection.mycomputername)) #! send client computer name to server.
		#receive data from server
		while True:
			try:
				self.message = self.sock.recv(1024) 
				self.dec_message = self.DecryptMessage(self.message) #!convert encrypted message into clear text using our mechanism
			except ConnectionAbortedError:
				#!if main thread gives quit signal.
				print("\nConnection Ended successfully, Program Will Now Quit.")
				sleep(0.5)
				exit()
			#self.dec_message = self.dec_message.decode()
			#self.dec_msfrecvd=self.dec_msfrecvd.decode()
			if "CP:" in self.dec_message: #! every message having (CP) is sended by our server to give us its name.
				self.server_computername = self.dec_message.split("CP:")[1]
				self.dec_message = ""
			if self.dec_message == "code:542": #! just to validate the connection ie. we are receiving messages properly (kind of checker)
				#!connection validated.
				print('[!] connection validated.')
				self.dec_message = ""
				pass
			if self.dec_message == 'connection:notaccepted':
				#!server denies your connection.
				self.sock.close()
				print('[-] Server Refused Your Connection Request.')
				break
			#!everything is good then we will be here.
			self.inital_step = True
			if len(self.dec_message) != 0: #! we will not handle empty message, only usefull message :p
				print("\n%s: %s"%(self.server_computername,self.dec_message))
				pass
		pass


try:
	x=EstablishConnection()
except KeyboardInterrupt:
	exit(1)
