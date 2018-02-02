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

        #Shifters
        self.shifter = wpilib.DoubleSolenoid(1,2)
        
        #User Inputs
        self.xboxController = wpilib.XboxController(0)

        #Setup Logic
        self.rightDriveMotors = wpilib.SpeedControllerGroup(self.motor3,self.motor4)
        self.leftDriveMotors = wpilib.SpeedControllerGroup(self.motor1,self.motor2)
        self.robotDrive = DifferentialDrive(self.leftDriveMotors, self.rightDriveMotors)
        self.rightIntakeMotors = wpilib.SpeedControllerGroup(self.stage1Right, self.stage2Right, self.stage3Right)
        self.leftIntakeMotors = wpilib.SpeedControllerGroup(self.stage1Left, self.stage2Left, self.stage3Left)

    def teleopPeriodic(self):

        #Drive
        self.robotDrive.arcadeDrive(self.xboxController.getX(0), self.xboxController.getY(0))

        #Intake
        self.rightIntakeMotors.set(self.xboxController.getY(1))
        self.leftIntakeMotors.set(self.xboxController.getY(1))

        #Shifting
        if self.xboxController.getAButtonPressed():
            self.shifter.set(wpilib.DoubleSolenoid.Value.kForward)
        if self.xboxController.getBButtonPressed():
            self.shifter.set(wpilib.DoubleSolenoid.Value.kReverse)

if __name__ == "__main__":
    wpilib.run(MyRobot)
