# -*- coding: utf-8 -*-
"""
    IMU & CAM server
    20.01.2020
    Version 1.0
    by Dipl.-Ing (FH) Sebastian Keidler, M. Sc. 
    ADrive LivingLab Kempten
"""

__author__ = "Dipl.-Ing(FH) Sebastian Keidler"
__version__ = "1.0"
__email___ = "sebastian.keidler@hs-kempten.de"
__status__ = "Develop"


# server.py
import struct
import ctypes
import socket
import time
import binascii
import sys, math
import pandas as pd
import os


print('IMU & CAM Server starts')

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

print('local machine name',host)
port = 9990
ip = '10.5.11.66'

# bind to the port
serversocket.bind((ip, port))
print('bind')

# queue up to 5 requests
serversocket.listen(5)
print('listen')




pathimg = 'data/img/'
pathdata = 'data/'

img = 'movie-0000.png'

'movie-000'+str(0)+'.png'

data = 'CM_FlatEarth_R5_to_CRO_withoutOffset_20200120_v1-0_SK.csv'
# open image to binary
def openIMG(pathimg,img):
    with open(pathimg+img, "rb") as image:
        f = image.read()
        b = bytearray(f)
    return b

# open IMU data
df = pd.read_csv(pathdata+data,sep=',')


i = 0
# establish a connection
clientsocket,addr = serversocket.accept()
print("1. Got a connection from %s" % str(addr))


while True:
    print('*SENT DATA ******')


    #Recieve Data from client
    data = clientsocket.recv(1024)
    
    #image name
    if i < 10 :
        name = 'movie-000'+str(i)+'.png'
    elif i < 100:
        name = 'movie-00'+str(i)+'.png'
    elif i < 1000:
        name = 'movie-0'+str(i)+'.png'
    elif i < 10000:
        name = 'movie-'+str(i)+'.png'

    
    # parse the data
    b = bytearray(data)

    res1 = struct.unpack("IfIffffffIIIIIIIfffffff",b)
    
    # 257 is request for data
    if res1[0] == 257:
        print('recieved 257 0x201')
        
        meta = struct.pack("IfIffffffIIIIIIIfffffff",
                res1[0],
                df['Time'].values[i],
                res1[2],
                res1[3],
                res1[4],
                df['Car.Road.GCS.Lat'].values[i],
                df['Car.Road.GCS.Long'].values[i],
                res1[7],
                res1[8],
                res1[9],
                res1[10],
                res1[11],
                res1[12],
                res1[13],
                res1[14],
                res1[15],
                res1[16],
                res1[17],
                res1[18],
                res1[19],
                res1[20],
                res1[21],
                res1[22]
             )
        print(df['Time'].values[i])
        print(df['Car.Road.GCS.Lat'].values[i])
        print(df['Car.Road.GCS.Long'].values[i])
        clientsocket.send(meta)
        
        
        
        
        print(struct.unpack("IfIffffffIIIIIIIfffffff",meta))
        
    
    
    
    
    
    
    #Recieve Data from client
    data1 = clientsocket.recv(1024)
    
    
    #if data == :
        
    print('*********************')
    print(data1)
    print(len(data1))
    print('*********************')

    # parse the data
    b1 = bytearray(data1)

    print(len(b1))

    res11 = struct.unpack("IfIffffffIIIIIIIfffffff",b1)
    
    
    #print(df['Time'].values[100])
        
        #clientsocket.close()
        
        
        
    # 258 is request for camera data  
    if res11[0] == 257:
        

        
        with open(pathimg+name, "rb") as image:
            f = image.read()
            b = bytearray(f)
            l1 = sys.getsizeof(b)
            
                   
        meta = struct.pack("IfIffffffIIIIIIIfffffff",
                res1[0],
                df['Time'].values[i],
                res1[2],
                res1[3],
                res1[4],
                df['Car.Road.GCS.Lat'].values[i],
                df['Car.Road.GCS.Long'].values[i],
                res1[7],
                res1[8],
                res1[9],
                int(len(f)),
                res1[11],
                res1[12],
                res1[13],
                res1[14],
                res1[15],
                res1[16],
                res1[17],
                res1[18],
                res1[19],
                res1[20],
                res1[21],
                res1[22]
             )
        
        clientsocket.send(meta)
        print(int(l1))
        
    
    #Recieve Data from client
    data2 = clientsocket.recv(1024)
    
    
    #if data == :
        
    print('*********************')
    print(data2)
    print(len(data2))
    print('*********************')

    # parse the data
    b2 = bytearray(data2)

    print(len(b2))

    res12 = struct.unpack("IfIffffffIIIIIIIfffffff",b2)        
        
    # 258 is request for camera data  
    if res12[0] == 258:
        
        print('recieved 258 0x202')
        print(res12[0])
        

        with open(pathimg+name, "r") as image:
            f = image.read()
           # b = bytearray(f)
            #l1 = sys.getsizeof(b)

            
            clientsocket.send(f)
        #f1.close()
        print("Done sending...")
        
        
         
    #clientsocket.close()
    print('*SENT THE NEXT DATA ******')
    i = i + 1
    print(i)