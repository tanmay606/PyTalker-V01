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
from os import environ #!to capture computer name 
import threading,socket #!to implement threading and socket programming.
from hashlib import sha1 #! we will use sha1 to encrypt our messages.
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
				print('Encryption Key Found, Please Ensure Client Have Same %s Key File.'%EstablishProgram.securitykeyfilename)
		except FileNotFoundError:
			#!key deleted or not generated (first time)
			print("Encryption Key Not Found, Generating Now. . . ")
			self.GenerateKey()
	def GenerateKey(self):
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
		decrypted_text=decrypted_text.decode()
		return decrypted_text

class EstablishProgram(threading.Thread,AuthenticateProgram):
	securitykeyfilename = "security.key" #!key file ( you don't have to change this.)
	server_port = 4545 #!must be same as client port
	server_lhost = "192.168.1.5" #!local address of server.
	try:
		server_computername = "CP:"+environ['COMPUTERNAME'] #!our computer name.
	except KeyError:
		server_computername = 'CP:Server'
	"""
	Structure where it binds the connection ie.establish open port for our job and listen for client connections.
	"""
	def __init__(self):
		AuthenticateProgram.__init__(self,EstablishProgram.securitykeyfilename)
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
		"""
		print(banner)
		threading.Thread.__init__(self)
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		print("[+] socket developed on server [success]")
		self.sock.bind(("",EstablishProgram.server_port))
		print("[!] server listening on %s:%s"%(EstablishProgram.server_lhost,EstablishProgram.server_port))
		self.sock.listen(5)
		print('[!] server socket now on listening mode.')
		print('(Press Enter To Keep Conversation Going.)')
		print("______________________________________________")
		pass
	def RealTimeSender(self):
		#!if we want to send msg.
		while True:
			self.message = input("(You) ")
			if self.message == "":
				#!not tolerate empty messages.
				pass
			else:
				self.enc_message = self.EncryptMessage(self.message) #!encrypting your messages.
				#!message will be first encrypted then send to client.
				self.client.sendall(self.enc_message) #! sending it to client.
				pass		
	def RealTimeReceiver(self):
		#!keep receiving client msg.
		while True:
			self.dec_message = self.DecryptMessage(self.client.recv(1024))
			if "CP:" in self.dec_message:
				#if computer name received of client then save it to use it furthur.
				self.client_computername = self.dec_message.split("CP:")[1]
				self.dec_message = ""
			if len(self.dec_message) != 0: #! not tolerate empty messages.
				print("\n%s: %s"%(self.client_computername,self.dec_message))


	def SearchClient(self):
		self.sendserver_computername = EstablishProgram.server_computername
		self.validation_code = "code:542"
		#self.validation_code = self.validation_code.encode()
		self.sendserver_computername = self.EncryptMessage(self.sendserver_computername)
		self.validation_code = self.EncryptMessage(self.validation_code)
		self.connection_denied = 'connection:notaccepted'
		self.connection_denied = self.EncryptMessage(self.connection_denied)
		while True:
			self.client,self.address=self.sock.accept()
			self.auth=input('[?] client %s wants to connect to chat, connect ? [Y/N] : '%self.address[0])
			if self.auth == 'y' or self.auth == 'Y':
				self.client.sendall(self.sendserver_computername)
				self.client.sendall(self.validation_code)
				pass
			elif self.auth == 'n' or self.auth == 'N':
				self.client.sendall(self.connection_denied)
				self.client.close()
				continue
				#reject the request.
				pass
			else:
				pass
			print("connected to client : ",self.address[0])
			thread1=threading.Thread(target=self.RealTimeReceiver)
			#thread2=threading.Thread(target=self.RealTimeSender)
			print('chat-bot started.\n')
			thread1.start()
			#!below code will act under main thread.
			while True:
				self.message = ""
				try:
					self.message = input("(You) ")
				except KeyboardInterrupt:
					self.quitmsg=input('\n[?] Do you really want to close chat with %s [Y/N] ? '%self.address[0])
					if self.quitmsg == 'y' or self.quitmsg == 'Y':
						#!user wants to quit this program.
						self.client.close()
						break
					elif self.quitmsg == 'n' or self.quitmsg == 'N':
						#!ignore it.
						pass
					else:
						#!ignore it.
						pass

				if self.message == "":
					pass
				else:
					self.enc_message = self.EncryptMessage(self.message)
					#!message will be first encrypted then send to client.
					self.client.sendall(self.enc_message)
					pass

		pass




x = EstablishProgram()
x.SearchClient()