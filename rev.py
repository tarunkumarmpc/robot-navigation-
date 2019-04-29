 #! /usr/bin/python3
"""

This console application demonstrates "set max velocity" feature of Fire Bird Robot during safety OFF condition.

This code demonstrates how to set maximum velocity of robot during safety OFF feture on Fire Bird Robot.
This maximum velocity will be set in terms of m/Sec.

In this spplication left as well as right velocity for both motors are set to 0.35m/Sec and max velocity is set to 0.13 m/Sec.
Since max velocity is specified, robot will compare velocity mentioned for "setLeftMotorVelocity_meterspersec" and "setRightMotorVelocity_meterspersec"
functions with velocity specified in "setRobotMaxVelocity_meterspersec" function, and robot will only obey min velocity.

This application uses ctype foreign function library for python and that allows calling a functions from DLLs or shared libraries.  

"""

from ctypes import * # importing ctypes from ctypes
import sys            
import os
import time

Position_Mode = c_ubyte(1) #c_ubyte = unassigned char 
Accelearation = c_ubyte(8)
Safety_ON = c_ubyte(1)
Safety_OFF = c_ubyte(0)
TimeOut = c_ubyte(0)


#TO RECEVIE GPS 
v = '0.0####0.0####\x00####\x00####0####0'
f = open('v.txt','w')
f.write(str(v))
f.close()


# TO RECEVIE VELOCITY 

multicast_group = '224.3.29.71'
server_address = ('', 10000)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


sock.bind(server_address)

group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    mreq)


while True:

    data, address = sock.recvfrom(1024)
    v = data.decode()
    f = open('K.txt','w')
    f.write(v)
    f.close()
f = open('K.txt','w')
f.write(str(K))
f.close()



if sys.platform.startswith('win32'): 
	ComPort = b"\\\\.\\COM3" #communication port (usb port)if your using windows
elif sys.platform.startswith('linux'):
	ComPort = b"/dev/ttyUSB0" # usb port if your using linux 

if sys.platform.startswith('win32'):
	libraryPATH = os.path.join(os.getcwd(),"FireBirdCLibrary.dll")
elif sys.platform.startswith('linux'):
	libraryPATH = os.path.join(os.getcwd(),"libFireBirdCLibrary.so") #we will be using the file in the directory and libraryPATH = os.path repersents the path of the file and we can use and see it accordingly these are in the form of strings
	
lib = CDLL(libraryPATH)

def open_comport(Com):
	hcomm = lib.connect_comm(Com) # connecting the communication port 
	return hcomm

message = ""
if True:
	while True :

		try:
			f = open('v.txt','r')
			for line in f:
				updated_message = line
				break
			
			f.close()
			#print("@@@@@@@@@@")
			#print(updated_message)
			#print(message)
			#print("@@@@@@@@@@")
			if updated_message != message:
				#print("Initial velocity : "+str(v)+"\nUpdated velocity : "+updated_v)
				message = updated_message

				args = message.split("####")
				print(args)
				gpsLatitude = c_float(float(args[0]))
				gpsLongitude = c_float(float(args[1]))
				gpsDirection_NS = c_char(' ' if args[2] == "\x00" else args[2])
				gpsDirection_EW = c_char(' ' if args[3] == "\x00" else args[3])
				gpsSatLock = c_ubyte(int(args[4]))
				gpsSatFix = c_ubyte(int(args[5]))
				print(gpsLatitude1,gpsLongitude1)
				time.sleep(3)




			
	
		except ValueError:
			print(args)



 		while True:
                               
        if lib.getGPSdata(hcomm,c_ulong(MAXBUFFERSIZE),gpsStringArray,byref(gps_struct)):
            for i in gpsStringArray:                                                        #Print string all strings received from GPS
                print (chr(i),end='')

            print('\n')
            print("Latitude = ",gps_struct.gpsLatitude)                                     #GPS latitude
            print("Longitude = ",gps_struct.gpsLongitude)                                   #GPS longitude
            print("Direction E/W = ",(gps_struct.gpsDirection_EW).decode("utf-8"))          #Direction East/West
            print("Direction N/S = ",(gps_struct.gpsDirection_NS).decode("utf-8"))          #Direction North/South
            print("No. of satellite locked = ",gps_struct.gpsSatLock)                       #GPS satellite lock
            print("No. of satellite fixed = ",gps_struct.gpsSatFix)                         #GPS satellite fix
            


            message = str(gps_struct.gpsLatitude2)+"####"+str(gps_struct.gpsLongitude2)+"####"+str((gps_struct.gpsDirection_NS).decode("utf-8"))+"####"+str((gps_struct.gpsDirection_EW).decode("utf-8"))+"####"+str(gps_struct.gpsSatLock)+"####"+str(gps_struct.gpsSatFix)
            sent = sock.sendto(str(message).encode(), multicast_group)
            print(message)
            print(message.split("####"))
            print(gpsLatitude2,gpsLongitude2)



lat1= radians(gpsLatitue1)
lon1= radians(gpsLongitude1)
lat2  =  radians(gpsLatitue1)
lon2= radians(gpsLongitude2)


radius = 3959 # km  3959

dlat = math.radians(lat2-lat1)
dlon = math.radians(lon2-lon1)
a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
     * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)

c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
d = radius * c
print(d)
d=d*1000
v = 1.66                                       #velocity of  the master robot
v_c =c_float(v)
y=  1.55
y_c = c_float(y)

def set_motor_parameters(handle): #these parameters are defined in the library 
    if lib.setMode(handle,Position_Mode):
        lib.DelaymSec(handle,c_ulong(50))
        if lib.setSafety(handle,Safety_OFF):
            if lib.setAcceleration(handle,Accelearation):
                if lib.setSafetyTimeout(handle,TimeOut):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False                
    else:
        return False


hcomm = c_void_p(0)

hcomm = open_comport(ComPort)                                                               #Open communication port




if hcomm != 0: #hcomm shouldn't be zero it means the device must be coonected to the robot otherwise the code will not run.

    if set_motor_parameters(hcomm):                                                         #Set motor parameters like safety feature,time out,acceleration and position mode control                                                       
        pass
    else:
        lib.disconnect_comm(hcomm)  # if it is disconnected we cannot set the parameters
        print ('set_motor_parameters() Fail\n')
    if lib.setLinearVelocity_meterspersec(hcomm, v_c):
    #if lib.setRobotAngularVelocityRadianpersec(hcomm, v_c):                        
        pass
    if lib.forward(hcomm):                                                                  #Motion forward
        pass

   
   
    if lib.getLeftMotorCount(hcomm,byref(leftEncoderCount)):                                #get left encoder count 
        print ("Left Encoder Count = ",leftEncoderCount.value)

    k= leftEncoderCount.value

    D=k/3840

    D=D/1000

 # receving velocity from the master 
    while True :

    	try:
    		f = open('K.txt','r')
    		updated_v = f.read()
    		f.close()
    		if float(updated_v) != v:
    			print("Initial velocity : "+str(v)+"\nUpdated velocity : "+updated_v)
    			v = float(updated_v)

    			v_c = c_float(v)
    			lib.setLinearVelocity_meterspersec(hcomm, v_c)
    			lib.forward(hcomm)
        if lib.getLeftMotorCount(hcomm,byref(leftEncoderCount)):                                #get left encoder count 
        print ("Left Encoder Count = ",leftEncoderCount.value)

        k= leftEncoderCount.value



       D=k/3840

       D=D/1000

if d=D
 if lib.stop(hcomm):                                                                     #Motion stop
        pass
 
else
    lib.setLinearVelocity_meterspersec(hcomm, v_c)
    	lib.forward(hcomm)

    if lib.resetMotorEncoderCount(hcomm):
        pass


	

else:
	print ("CAN NOT ESTABLISH COMMUNICATION\n")        
	lib.disconnect_comm(hcomm)
	

