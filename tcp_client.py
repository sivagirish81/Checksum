from socket import *
from functools import reduce

serverName = "127.0.0.1"
serverPort = 12000

def wrap_add(a, b):			# a and b are binary string, we have to do udp style wrap adding
	c = bin(int(a,2) + int(b,2))[2:]			# add a and b in binary format and clip the intial '0b'
	if(len(c) == 8):							# if overflow happened, wrap around
		c = bin(int(c[1:],2) + int('1',2))		
	return c[2:].zfill(7)						#make sure 7 bits and send back


def compute_checksum(sentence):
	binary_padded_equivalent = [format(ord(i), 'b').zfill(7) for i in sentence]
	wrapped_result = reduce(wrap_add, binary_padded_equivalent)
	return wrapped_result

def complement(wrapped_value):
	return ''.join(str(int(i,2)^1) for i in  wrapped_value) 

def read_file(file_path):
	fd = open(file_path, 'r')
	content = [x.strip() for x in fd.readlines()]
	print(content)
	fd.close()
	return content

def sent_successfully(line):

	checksum = complement(compute_checksum(line))
	packet = line + "\n" + checksum 		#last line will always be checksum
	clientSocket.send(packet.encode())

	acknowledgement_message = clientSocket.recv(1024).decode()		#ACK or NAK depending on whether message was received without corruption
	if(acknowledgement_message == "ACK"):
		return True
	else:
		return False
		


clientSocket = socket(AF_INET, SOCK_STREAM)					
clientSocket.connect((serverName,serverPort))
file_path = input("Input absolute file path")

content = read_file(file_path)

for line in content:
	if(sent_successfully(line)):
		continue
	else:
		print("Packet Loss, message was corrupted when received by Sender")
		exit()

print("Message received by Sender")

clientSocket.close()