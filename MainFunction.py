
import FPS, sys,time,socket
DEVICE_GPIO = '/dev/ttyS0' #for raspberry 
DEVICE_LINUX = '/dev/cu.usbserial-A601EQ14'
DEVICE_MAC = '/dev/cu.usbserial-A601EQ14'
DEVICE_WINDOWS = 'COM3'
FPS.BAUD = 9600
FPS.DEVICE_NAME = DEVICE_GPIO
host=''
port=1234
id=0
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((host,port))
sock.listen()
clientaddress=sock.accept()
def Enroll(fps):
    '''
    Enroll test
    '''
    fps.SetLED(True)
    enrollid=0
    okid=True
    #search for a free enrollid, you have max 200
    message="wait until the id no. is allotted\n"
    sock.sendall(message)
    while okid and enrollid < 200:
        okid = fps.CheckEnrolled(enrollid)
        print"alloting id no."
        if okid:
            enrollid+=1
            
            #print enrollid,okid
            #print 'this is the enroll id'
    if enrollid <200:
        #press finger to Enroll enrollid
        print 'Press finger to Enroll for first capture %s' % str(enrollid)
        message1="id. allocated is "+str(enrollid)+"\nPress finger to start enrollment\n"
        sock.sendall(message1)
        time.sleep(0.2)
        fps.EnrollStart(enrollid)
        while not fps.IsPressFinger():
            print'Press finger'
            sock.send("press finger\n")
            FPS.delay(0.2)
        iret = 0
        if fps.CaptureFinger(True):
            time.sleep(0.2)
            #remove finger
            print 'remove finger'
            sock.sendall("remove finger\n")
               
            fps.Enroll1()
            fps.SetLED(False)
            time.sleep(0.2)
            #print 'Enrollment 1 successfull'
            fps.SetLED(True)
            while not fps.IsPressFinger():
                FPS.delay(0.2)
            #Press same finger again
            print 'Press same finger again'
            sock.sendall("press same finger again\n")
            while not fps.IsPressFinger():
                FPS.delay(0.1)
            if fps.CaptureFinger(True):
                #remove finger
                time.sleep(0.1)
                print 'remove finger'
                sock.sendall('remove finger\n')
                fps.Enroll2()
                fps.SetLED(False)
                time.sleep(0.1)
                #print 'Enrollment 2 successfull'
                fps.SetLED(True)
                while not fps.IsPressFinger():
                    FPS.delay(0.1)
                #Press same finger again
                print 'press same finger yet again'
                sock.sendall('press same finger yet again\n')
                while not fps.IsPressFinger():
                    FPS.delay(0.1)
                if fps.CaptureFinger(True):
                    #remove finger
                    iret = fps.Enroll3()
                    time.sleep(0.1)
                    fps.SetLED(False)
                    #print 'Enrollment successfull'
                    if iret == 0:
                        print 'Enrolling Successfull'
                        sock.sendall('Enrolling Successful\n')
                    else:
                        print 'Enrolling Failed with error code: %s' % str(iret)
                        sock.sendall('Enrolling Failed with error code:'+str(iret)+'\n')
                else:
                    print 'Failed to capture third finger'
                    sock.sendall('Failed to capture third finger\n')
            else:
                print 'Failed to capture second finger'
                sock.sendall('Failed to capture second finger\n')
        else:
            print 'Failed to capture first finger'
            sock.sendall('Failed to capture first finger\n')
    else:
        print 'Failed: enroll storage is full'
        sock.sendall('Failed: enroll storage is full\n')

def identify1_n(fps):
    fps.SetLED(True)
    sock.sendall('Press finger\n')
    while not fps.IsPressFinger():
        FPS.delay(0.1)
        print 'Press finger'
    
    if fps.CaptureFinger(True):
        time.sleep(0.1)
        print"remove finger"
        sock.sendall('Remove finger\n')
        id_identify=fps.Identify1_N()
        print "id is",id_identify
        sock.sendall('id is :'+str(id_identify))
    fps.SetLED(True)
        

def delete(fps):
    id=sock.recv(1024)
    id=int(id[0])
    fps.DeleteID(id)
    print "id no. :",id," is deleted"
    sock.sendall("id no. :"+str(id)+" is deleted\n")


def deleteall(fps):
    fps.DeleteAll()
    print "database is cleared"
    sock.sendall('database is cleared\n')


def Verify1_1(fps):
    fps.SetLED(True)
    id=sock.recv(1024)
    id=int(id[0])
    sock.sendall('Press finger\n')
    while not fps.IsPressFinger():
        FPS.delay(0.1)
        print 'Press finger'
    
    if fps.CaptureFinger(True):
        time.sleep(0.1)
        if fps.Verify1_1(id)==0:
            print"yes!!id and fingerprint matched."
            sock.sendall("yes!!id and fingerprint matched.")
        else:
            print"oops!!id and fingerprint not matched."
            sock.sendall("oops!!id and fingerprint not matched.")
    fps.SetLED(True)




    
if __name__ == '__main__':
    fps = FPS.FPS_GT511C3(device_name=DEVICE_GPIO,baud=9600,timeout=2,is_com=False) #settings for raspberry pi GPIO
    options = { 1 : Enroll,
                2 : identify1_n,
                3 : delete,
                4 : deleteall,
                5 : Verify1_1,
    }
    #input=int(input("1:enroll \n2:identify \n3:delete \n4:deleteall \n5:verify1_1\n"))
    input=client.recv(1024)
    input=int(input[0])
    options[input](fps)






    
