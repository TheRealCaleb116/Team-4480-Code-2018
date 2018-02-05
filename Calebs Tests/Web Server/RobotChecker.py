import wpilib
from networktables import NetworkTables
import time
import multiprocessing

#global toggle Variables
global BatteryOut
BatteryOut = False


def Start(robotIP,Q):
    global queue
    queue = Q

    NetworkTables.initialize(server=robotIP)
    sd = NetworkTables.getTable('SmartDashboard/Data')
    sd.addSubTableListener(Check)



def Check(key,value,isNew):

    if (key == "batteryVoltage"):
        Battery(value)
    elif (key == "GamePeriod"):
        GamePeriod()


#Handlers
def Battery(value):
    if (value <= 10):
        if (BatteryOut == False):
            queue.put("Battery:True")
            BatteryOut = True
    else:
        if (BatteryOut == True):
            queue.put("Battery:False")
            BatteryOut = False

def GamePeriod(value):
    if (value == "Teleop"):
        queue.put("GamePeriod:True")
