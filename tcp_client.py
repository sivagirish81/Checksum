from socket import *
from functools import reduce
import sys

serverName = "127.0.0.1"
serverPort = 12000

if(len(sys.argv) != 2):
	print("Wrong usage, please input a code 1 - not error, 2 - error")
	exit(1)


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
	content = fd.read()
	fd.close()
	return content

clientSocket = socket(AF_INET, SOCK_STREAM)			
clientSocket.connect((serverName,serverPort))
file_path = input("Input absolute file path")

content = read_file(file_path)
contentws = content.replace("\n"," ")

checksum = complement(compute_checksum(contentws))

packet = content + "\n" + checksum 		#last line will always be checksum

if(sys.argv[1] == "2"):					#introduce error
	packet = "error" + packet 

print("Sent Message:", packet)
clientSocket.send(packet.encode())

acknowledgement_message = clientSocket.recv(1024*1024).decode()		#ACK or NAK depending on whether message was received without corruption

if(acknowledgement_message == "ACK"):
	print("Message received by Sender")
else:
	print("Packet Loss, message was corrupted when received by Sender")

clientSocket.close()