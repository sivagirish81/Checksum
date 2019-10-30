from socket import *
from functools import reduce

def wrap_add(a, b):			# a and b are binary string, we have to do udp style wrap adding
	c = bin(int(a,2) + int(b,2))[2:]			# add a and b in binary format and clip the intial '0b'
	if(len(c) == 8):							# if overflow happened, wrap around
		c = bin(int(c[1:],2) + int('1',2))		
	return c[2:].zfill(7)						#make sure 7 bits and send back


def compute_checksum(sentence):
	binary_padded_equivalent = [format(ord(i), 'b').zfill(7) for i in sentence]
	wrapped_result = reduce(wrap_add, binary_padded_equivalent)
	return wrapped_result


def extract_checksum(sentence):
	checksum = sentence.split("\n")[-1]
	return checksum

def extract_message(sentence):	
	message = '\n'.join(sentence.split("\n")[:-1])
	return message

def validate_checksum(received_checksum, computed_checksum):
	c = bin(int(received_checksum,2) + int(computed_checksum,2))[2:]
	return c == '1111111'

serverPort = 12000

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)
print("The server is ready to receive")
while True:
	connectionSocket, addr = serverSocket.accept()

	sentence = connectionSocket.recv(1024*1024).decode()
	output_fd = open("output.txt", "w")
	output_fd.write(sentence)
	output_fd.close()
	#print("\n**************",sentence,end="***********\n")
	received_checksum = extract_checksum(sentence)
	print("Received checksum:", received_checksum)

	message = extract_message(sentence)
	print("Received message")
	print(message)

	computed_checksum = compute_checksum(message.replace("\n"," "))


	if(validate_checksum(received_checksum, computed_checksum)):
		acknowledgement_message = "ACK"
	else:
		acknowledgement_message = "NAK"

	connectionSocket.send(acknowledgement_message.encode())


	connectionSocket.close()