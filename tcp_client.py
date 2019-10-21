from socket import *
# serverName = input("Enter the serverName")
# serverPort = int(input("Enter the port name"))

serverName = "127.0.0.1"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
sentence = input("Input lowercase sentence:")

clientSocket.send(sentence.encode())
clientSocket.send((sentence+"bla").encode())

modifiedSentence = clientSocket.recv(1024).decode()
print('From Server:', modifiedSentence)
clientSocket.close()