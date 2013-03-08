#Rajiev Timal SMTP Programming Lab

from socket import *
msg = "\r\n I love computer networks!"
endmsg="\r\n.\r\n"
mailfrom = "MAIL FROM:<RTimal@mb92d36d0.tmodns.net>\r\n"
rcptto="RCPT TO:<rtimal@gmail.com>\r\n"
data = "DATA\r\n"
quitmsg="QUIT\r\n"
subject = "Subject: Computer Networks SMTP Programming project Test\r\n"


#choose a mail server
mailserver="gmail-smtp-in.l.google.com"
port=25
connectaddress=(mailserver,port)

# create socket called clientSocket and establish a TCP connection with mailserver
clientSocket=socket(AF_INET,SOCK_STREAM)
clientSocket.connect(connectaddress)
recv=clientSocket.recv(1024)
print(recv)
if recv[:3].decode()!='220':
    print("220 reply not received from server")

#Send HELO command and print server response.
heloCommand="HELO Alice\r\n"
clientSocket.send(bytes(heloCommand.encode()))
recv1=clientSocket.recv(1024)
print(recv1)
if recv1.decode()[:3]!="250":
    print("250 reply not received from server.")

#Send MAIL FROM command and print server response.
clientSocket.send(bytes(mailfrom.encode()))
recv2=clientSocket.recv(1024)
print(recv2)

#Send RCPT TO command and print server response.
clientSocket.send(bytes(rcptto.encode()))
recv3=clientSocket.recv(1024)
print(recv3)

#Send DATA command and print server response.
clientSocket.send(bytes(data.encode()))
recv4=clientSocket.recv(1024)
print(recv4)

#send message data.
#message ends with a single period.
#period has to be concatenated in the same send to the request, or it hangs on the send waiting for a period in the message string
#subject line was added
clientSocket.send(bytes((mailfrom+subject+msg+endmsg).encode()))
recv5=clientSocket.recv(1024)
print(recv5)

#send QUIT command and get server response.
clientSocket.send(bytes(quitmsg.encode()))
recv7=clientSocket.recv(1024)
print(recv7)

print ("Mail sent")

