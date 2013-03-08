#import socket module
#Rajiev Timal - 0220052 - Computer Networking programming Lab # 1
from socket import *    


serverSocket = socket(AF_INET, SOCK_STREAM)
host = ''
port =1225
serverSocket.bind((gethostbyname(gethostname()),port))
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.listen(1)
print('Ready to serve')

while  True:
    (connectionSocket, address)=serverSocket.accept()
    try:
        message = connectionSocket.recv(8192)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = ''
        while 1:
            line = f.readline()
            outputdata += line
            if not line:
                break
        #connectionSocket.send(str.encode('HTTP/1.1 200 OK'))
        #For some reason, after i send the header indicated above , The content (outputdata , cant be sent)
        connectionSocket.send(str.encode(outputdata))
        connectionSocket.close()
        break
    except IOError:
        filenotfound='File not found, 404 error'
        connectionSocket.send(str.encode(filenotfound))
        connectionSocket.close()
        break
    

serverSocket.close()  
