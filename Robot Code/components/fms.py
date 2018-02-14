#!/usr/bin/env python3
import wpilib

class Fms(object):
    
    def __init__(self):
        self.driverStation = wpilib.DriverStation.getInstance()
        print(self.driverStation.getAlliance())

    def getFms(self):
        if self.driverStation.getAlliance() == 1:
            print('Blue')
        elif self.driverStation.getAlliance() == 2:
            print('Invalid Alliance')
        elif self.driverStation.getAlliance() == 0:
            print('Red')
        else:
            print('failed')

