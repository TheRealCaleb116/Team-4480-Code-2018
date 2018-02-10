import wpilib
from networktables import NetworkTables
import time
import multiprocessing




def Check(source, key, value, isNew):

    if (key == "batteryVoltage"):
        Battery(value)
    elif (key == "GamePeriod"):
        GamePeriod(value)


#Handlers
def Battery(value):
    global BatteryOut

    if (value <= 10):
        if (BatteryOut == False):
            queue.put("Battery:True")
            BatteryOut = True
    else:
        if (BatteryOut == True):
            queue.put("Battery:False")
            BatteryOut = False

def GamePeriod(value):
    global inAuto
    
    if (value == "Autonomous"):
        queue.put("AutonomousPopup:True")
        inAuto = True

    elif (value == "Disabled" or value == "Teleop"):
        if (inAuto == True):
            queue.put("AutonomousPopup:False")
            inAuto = False


def Start(robotIP,Q):
    #Global variables
    global queue
    queue = Q

    global BatteryOut
    BatteryOut = False

    global inAuto
    inAuto = False


    #Start Everything
    NetworkTables.initialize(server=robotIP)
    sd = NetworkTables.getTable('SmartDashboard')

    sub = sd.getSubTable("Data")

    sub.addEntryListener(Check)

    while True:
        time.sleep(0.1)
        #print("running")
