#!/usr/bin/env python3
#
# Python3 Robot code: "Unititled" using Robotpy
# 2018 - 2018, 4480 "Forty48ie" "UC-Botics"
# This Code is protected by UC-Botics under the leadership of our profound and prominent
# Senior Mechanical Engineer: Ethan Robertson and hereby stands as an inspirations to all
# of us here to do great things.

import wpilib
import wpilib.buttons
import ctre
from wpilib.drive import DifferentialDrive        
class MyRobot(wpilib.IterativeRobot):


    def robotInit(self):

        #Drive Motors
        self.motor1 = ctre.WPI_TalonSRX(1)
        self.motor2 = ctre.WPI_TalonSRX(2)
        self.motor3 = ctre.WPI_TalonSRX(9)
        self.motor4 = ctre.WPI_TalonSRX(10)
        
        #Intake Motors
        self.stage1Left = ctre.WPI_TalonSRX(3)
        self.stage1Right = ctre.WPI_TalonSRX(4)
        self.stage2Left = ctre.WPI_TalonSRX(5)
        self.stage2Right = ctre.WPI_TalonSRX(6)
        self.stage3Left = ctre.WPI_TalonSRX(7)
        self.stage3Right = ctre.WPI_TalonSRX(8)
        
        
        #User Inputs
        self.xboxController = wpilib.Joystick(0)
        self.xboxAbutton = wpilib.buttons.JoystickButton(self.xboxController, 1)
        self.xboxBbutton = wpilib.buttons.JoystickButton(self.xboxController, 2)
        self.xboxYbutton = wpilib.buttons.JoystickButton(self.xboxController, 4)

        #Setup Logic
        self.robotDrive = wpilib.RobotDrive(self.motor1, self.motor2, self.motor3, self.motor4)

    def teleopPeriodic(self):
        
        #Drive
        self.robotDrive.arcadeDrive(self.xboxController.getX(), self.xboxController.getY())

        #Intake
        self.stage1Left.set(self.xboxController.getRawAxis(5))
        self.stage1Right.set(self.xboxController.getRawAxis(5))
        self.stage2Left.set(self.xboxController.getRawAxis(5))
        self.stage2Right.set(self.xboxController.getRawAxis(5))
        self.stage3Left.set(self.xboxController.getRawAxis(5))
        self.stage3Right.set(self.xboxController.getRawAxis(5))
      
if __name__ == "__main__":
    wpilib.run(MyRobot)
