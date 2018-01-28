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
        if (phase < 0 || phase > 2):
            raise Exception("You miss implamented the Update Status Method.")

        else:
            self.data.putNumber("GamePeriod",phase)

    def UpdateBatteryStatus(self):
        temp = self.driverStation.getBatteryVoltage()
        if (self.bVoltage == temp):
            return

        self.bVoltage = temp;
        #push value to data sub table
        self.data.putNumber("batteryVoltage",temp)

    def getAlliance(self):
        allience = self.driverStation.getAlliance()

        if (allience == DriverStation.Alliance.Blue):
            self.data.putString("Allience","Blue")
        elif (allience == DriverStation.Allience.Red):
            self.data.putString("Allience","Red")
        else:
            raise Exception("This should have happened. Error in getAllience()")

    def UpdateMatchTime(self):
        temp = self.driverStation.getMatchTime()
        self.data.putNumber("AproxMatchTime",temp)
