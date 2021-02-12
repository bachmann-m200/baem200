'''
Created on 05.08.2019

@author: neumann
'''
import time
import threading
import baem200.m1com as m1com
import opcua
from opcua import ua
from socket import socket, inet_aton, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST

def getProjectData(projectList, serialNb):
    """
    Get project data.

    Usage:

    >>> projectList = ""
    >>> serialNb = ""
    >>> getProjectData(projectList, serialNb)
    """
    for i in range(len(projectList)):
        if serialNb in projectList[i]:
            return projectList[i].copy()

def setIp(serialnb, newip, oldip='192.0.1.230',  ipmask='255.255.255.0'):
    """
    Set a different ip address for a device.

    Usage:

    >>> serialnb = ""
    >>> newip = 10.14.41.167
    >>> setIp(serialnb, newip)
    """
    ipmask = ipmask.split('.')
    ipmask.reverse()
    ipmask = '.'.join(ipmask)
    packetstart = b"\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x02\x20\x00\x10\x00\x00\x00\x00\x03\x00\x00\x01\x42\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    separator = b"\x00\x00"
    packetend = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    packet = packetstart + serialnb.encode() + separator + inet_aton(oldip) + inet_aton(newip) + inet_aton(ipmask) + packetend

    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
    s.sendto(packet,('255.255.255.255',3000))
    s.close()

def blinkDevice(serialnb):
    """
    Blink a device using its serial number

    Usage:

    >>> serialnb = ""
    >>> blinkDevice(serialnb)
    """
    packetstart = b"\x4c\xeb\xf5\x50\x00\x00\x00\x00\x00\x00\x00\x02\x20\x00\x10\x00\x00\x00\x00\x03\x00\x00\x01\x44\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    packetend = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    packet = packetstart + serialnb.encode() + packetend
 
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET,SO_BROADCAST,1)
    s.sendto(packet,('255.255.255.255',3000))
    s.close()

def addNewScadaDevice():
    """
    Add a new scada device

    Usage:

    >>> addNewScadaDevice()
    """
    client = opcua.Client('opc.tcp://10.11.31.40:4840')
    client.connect()
    atviseObject = client.get_node('ns=1;s=AGENT.OBJECTS.SCAMPY.newDefault.newDevice')
    atviseObject.set_value(ua.DataValue(ua.Variant(True,ua.VariantType.Boolean)))
    client.disconnect()

def findNewM1():
    """
    Find a new M1 target.

    Usage:

    >>> mh = findNewM1()
    """
    global devices
    devices = None
    foundnewdevice = False
    m1devices = m1com.M1TargetFinder().TargetBroadcastSmiPing()
    if m1devices == {}:
        print("no devices found")
    else:
        for m1 in m1devices.keys():
            newm1 = m1devices[m1]['hostAddr']
            if newm1 == '192.0.1.230':
                foundnewdevice = True
                if devices != None:
                    if m1devices[m1]['extPingR']['ProdNb'] != devices['extPingR']['ProdNb']:
                        devices = m1devices[m1]
                        break
                    else:
                        break
                else:
                    
                    devices = m1devices[m1]
                    print("found device:\n", devices)
                    projectdata = getProjectData(projectlist, devices['extPingR']['ProdNb'])
                    setIp(projectdata[0], projectdata[1], ipmask=projectdata[2])
                    #addNewScadaDevice()
                    blinkDevice(projectdata[0])
                    print("found device:\n", devices )
                    foundnewdevice = False
                    break
            else:
                foundnewdevice = False 

    if not foundnewdevice:
        devices = None

    #print(devices)
    time.sleep(10)
    scanthread = threading.Thread(target=findNewM1)
    scanthread.start()

def findM1(devicesData):
    """
    Find a M1 target.

    Usage:

    >>> devicesData = 0
    >>> mh = findM1(devicesData)
    """
    m1dll = m1com.PyCom()
    m1devices = m1com.M1TargetFinder(m1dll).TargetBroadcastSmiPing()
    if m1devices == {}:
        return False
    else:
        for m1 in m1devices.keys():
            device = m1devices[m1]            

            if device['extPingR']['ProdNb'] == devicesData[0]:
                    if device['hostAddr'].decode() == devicesData[1]:
                        return True
                    
                    blinkDevice(devicesData[0])
                    setIp(devicesData[0], devicesData[1], ipmask=devicesData[2])
                    
                    time.sleep(3)
                    
                    pingDevice = m1com.M1TargetFinder(m1dll).TargetSmiPing(devicesData[1])
                    
                    if pingDevice['ProdNb'] == devicesData[0]:
                        return True

                    return False
            else:
                continue

    return False

if __name__ == "__main__":

    import doctest
    doctest.testmod(verbose=False)