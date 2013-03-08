#Rajiev Timal - 0220052 - ICMP Pinger

from socket import *

import os
import sys
import struct
import time
import select
import binascii
import time

ICMP_ECHO_REQUEST = 8
packetssent=0
packetsreceived=0
#packetslost=(packetssent-packetsreceived)/packetssent
rttmin=999
rttmax=0
pinged=0
totalrtt=0

  ########################################################################
def checksum(str):
 csum = 0
 countTo = (len(str) / 2) * 2
 count = 0
 while count < countTo:
     thisVal = (str[count+1]) * 256 + (str[count]) 
     csumL = csum + thisVal
     csum = csum & 0xffffffff
     count = count + 2
 if countTo < len(str):
    csum = csum + ord(str[len(str) - 1])
    csum = csum & 0xffffffff
    
 csum = (csum >> 16) + (csum & 0xffff)
 csum = csum + (csum >> 16)
 answer = ~csum
 answer = answer & 0xffff
 answer = answer >> 8 | (answer << 8 & 0xff00)
 return answer
 
 ########################################################################
def receiveOnePing(mySocket, ID, timeout, destAddr):
 timeLeft = timeout
 while 1:
     startedSelect = time.time()
     whatReady = select.select([mySocket], [], [], timeLeft)
     howLongInSelect = (time.time() - startedSelect)
     if whatReady[0] == []: # Timeout
         bytesInDouble=struct.calcsize("d")
         print ("Reply from " + str(destAddr) + ":" + " bytes=" + str(bytesInDouble) + " " )
         return "Request timed out."
     timeReceived = time.time()
     recPacket, addr = mySocket.recvfrom(1024)
     global packetsreceived
     packetsreceived=packetsreceived+1
     icmpHeader = recPacket[20:28]
     ttl = struct.unpack("d", recPacket[0:8])[0]
     #ttl = print (rawPongHop)
     #ttl= int(binascii.hexlify(bytes(int(rawPongHop))), 16)
     
     type,code,checksum,packetID,sequence=struct.unpack("bbHHh", icmpHeader)
     
     if (packetID==ID):
         bytesInDouble=struct.calcsize("d")
         timeSent=struct.unpack("d",recPacket[28:28 + bytesInDouble])[0]
         print ("Reply from " + str(destAddr) + ":" + " bytes=" + str(bytesInDouble) + " " )
         return timeReceived - timeSent

     timeLeft = timeLeft - howLongInSelect
     if timeLeft <= 0:
         return "Request timed out."
 
  ########################################################################
def sendOnePing(mySocket, destAddr, ID):
 # Header is type (8), code (8), checksum (16), id (16), sequence (16)
 
 myChecksum = 0
 # Make a dummy header with a 0 checksum.
 # struct -- Interpret strings as packed binary data
 header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
 
 data = struct.pack("d", time.time())
 
 # Calculate the checksum on the data and the dummy header.
 myChecksum = checksum(header + data)
 
 # Get the right checksum, and put in the header
 if sys.platform == 'darwin':
     myChecksum = htons(myChecksum) & 0xffff
     #Convert 16-bit integers from host to network  byte order.
 else:
     myChecksum = htons(myChecksum)
 header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
 packet = header + data
 mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
 #Both LISTS and TUPLES consist of a number of objects
 #which can be referenced by their position number within the object.

 ########################################################################

 
def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    mySocket= socket(AF_INET, SOCK_RAW, icmp)
    mySocket.bind(("",0))
    myID = os.getpid() & 0xFFFF  #Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    global packetssent
    packetssent=packetssent+1
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay
  ########################################################################
 
def ping(host, timeout=1):
 #timeout=1 means: If one second goes by without a reply from the server,
 #the client assumes that either the client's ping or the server's pong is lost
 dest = gethostbyname(host)
 global pinged
 if(pinged ==0):
     print ("Pinging " + dest + " using Python:")
     print ("")
     pinged=1
 #Send ping requests to a server separated by approximately one second
 while 1 :
     delay = doOnePing(dest, timeout)
     if (delay=="Request timed out."):
         print(delay)
         print(" ")
     else:
         delay=delay*1000
         print("rtt = " + str(delay) +" ms")
         print(" ")
     time.sleep(1)# one second
     global totalrtt
     global rttmin
     global rttmax
     if (delay!="Request timed out."):
         if (delay<rttmin):
             rttmin=delay
         if (delay>rttmin):
             rttmax=delay
         totalrtt=totalrtt+delay
     return delay
    
 ########################################################################
hosttoping="tz.pool.ntp.org"
print("Pinging: "+hosttoping+" with 8 bytes of data")
for i in range (0,10):
    ping(hosttoping)

print("Ping Statistics for " +gethostbyname("www.poly.edu"))
print("")
print ("Packets: Sent = "+str(packetssent))
print ("Packets: Received = "+str(packetsreceived))
print ("Packets: lost =" +str(packetssent-packetsreceived))
if((packetssent-packetsreceived)>=0):
    print ("Packets: lost% = "+str(((packetssent-packetsreceived)/packetssent)*100))
else:
    print ("Packets: lost% = "+str(0))
    
print ("Minimum RTT: " + str(rttmin)+" ms")
print("Maximum RTT: " +str(rttmax)+" ms")
print("Average RTT: " +str(totalrtt/packetsreceived)+" ms")
