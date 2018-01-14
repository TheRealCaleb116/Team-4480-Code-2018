#!/usr/bin/env python3
# Python3 Robot code: "Unititled"
# 2017 - 2018, 4480 "Forty48ie" "UC-Botics"


import wpilib
import wpilib.buttons
from robotpy_ext.autonomous import AutonomousModeSelector
from robotpy_ext.common_drivers import units, navx
import networktables
from wpilib.drive import DifferentialDrive
import wpilib.drive
import math
import hal


print (wpilib.__version__)

class MyRobot(wpilib.IterativeRobot):


    def robotInit(self):


        #Motors
        self.leftMotorInput = wpilib.Talon(1) #  AEN
        self.rightMotorInput = wpilib.Talon(2) # AEN
     
        self.drive = wpilib.drive.DifferentialDrive(self.leftMotorInput, self.rightMotorInput)
      
      
        #Inputs
        self.xboxController = wpilib.Joystick(0)
        self.xboxAbutton = wpilib.buttons.JoystickButton(self.xboxController, 1)
        self.xboxBbutton = wpilib.buttons.JoystickButton(self.xboxController, 2)
        self.xboxYbutton = wpilib.buttons.JoystickButton(self.xboxController, 4)
       
       
       #Navigation and Logistics
        
       
       #Defining Variables


        #Auto mode variables
        #self.components = {
         #   'drive': self.drive
        #}
        #self.automodes = AutonomousModeSelector('autonomous', self.components)
    

    def autonomousPeriodic(self):

        #self.automodes.run()
        pass

    def teleopPeriodic(self):
        
        self.drive.tankDrive(self.xboxController.getY(), self.xboxController.getRawAxis(5))




if __name__ == "__main__":
    wpilib.run(MyRobot)

 
