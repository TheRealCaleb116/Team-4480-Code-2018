#This is the class with cclass to update networktables for the hud
#Ask Caleb if you cant figure out how to implament This

import wpilib
import networktables

class StatusUpdater (object):

    def __init__(self, RC, NT):
        #get robot instance and instance of network tables
        self.robotClass = RC
        self.netTable = NT

        #the subtable that will store our info
        self.data = self.netTable.getSubTable("Data")

        #get current driver station instance
        self.driverStation = wpilib.DriverStation.getInstance();

        #Random Vars
        self.bVoltage = -1;

    def UpdateStatus(self,phase):
        #Updates current phase period of play to network tables
        #0 - Disabled
        #1 - Autonomous
        #2 - teleop
        if (phase < 0 or phase > 2):
            raise Exception("You miss implamented the Update Status Method.")

        else:
            if (phase == 0):
                self.data.putString("GamePeriod","Disabled")
            elif(phase == 1):
                self.data.putString("GamePeriod","Autonomous")

            elif(phase == 2):
                self.data.putString("GamePeriod","Teleop")


    def UpdateBatteryStatus(self):
        temp = self.driverStation.getBatteryVoltage()
        if (self.bVoltage == temp):
            return

        self.bVoltage = temp;
        #push value to data sub table
        self.data.putNumber("batteryVoltage",temp)

    def getAlliance(self):
        alliance = self.driverStation.getAlliance()

        if (alliance == self.driverStation.Alliance.Blue):
            self.data.putString("Alliance","Blue")
        elif (alliance == self.driverStation.Alliance.Red):
            self.data.putString("Alliance","Red")
        else:
            raise Exception("This should have happened. Error in getAllience()")

    def UpdateMatchTime(self):
        temp = self.driverStation.getMatchTime()
        self.data.putNumber("AproxMatchTime",temp)
