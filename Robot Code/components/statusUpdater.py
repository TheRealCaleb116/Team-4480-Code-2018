#This is the class with cclass to update networktables for the hud
#Ask Caleb if you cant figure out how to implament This

import wpilib
import networktables

class StatusUpdater (object):

    def __init__(self, RC, NT):
        #get robot instance and instance of network tables
        self.robotClass = RC
        self.netTable = NT

        #the subtable that will store our infor
        self.data = self.netTable.getSubTable("Data")

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
        robotClass
