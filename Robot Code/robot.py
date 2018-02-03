#!/usr/bin/env python3
#
# Python3 Robot code: "Willie" using Robotpy 2018 - 2018, 4480 "Forty48ie" "UC-Botics" out of Upsala, Minnesota
# This Code is protected by ROBBY ACT under the leadership of our profound and prominent Senior Mechanical Engineer: Ethan Robertson
# and hereby stands as an inspirations to all of us here to do great things.
#
#
#
#
#

import wpilib
import wpilib.buttons
import ctre
from wpilib.drive import DifferentialDrive
import math
import hal
from networktables import NetworkTables
from robotpy_ext.common_drivers import units, navx
from robotpy_ext.autonomous import AutonomousModeSelector
from components import statusUpdater as SU
print (wpilib.__version__)


class MyRobot(wpilib.IterativeRobot):

    def disabledInit(self):
        
        #Update Allience
        self.statUpdater.getAlliance()
        
        #Send Data to Networktable
        self.statUpdater.UpdateStatus(0)
        self.statUpdater.UpdateMatchTime()

    def autonomousInit(self):
        self.statUpdater.UpdateStatus(1)
        self.statUpdater.UpdateMatchTime()
   
    def teleopInit(self):
        self.statUpdater.UpdateStatus(2)
        self.statUpdater.UpdateMatchTime()

    def robotInit(self):
        
        #Networktables
        self.netTable = NetworkTables.getTable('SmartDashboard')

        #Hud Data Handlers
        self.statUpdater = SU.StatusUpdater(self,self.netTable)

        #Drive Motors
        self.motor1 = ctre.WPI_TalonSRX(1)
        self.motor2 = ctre.WPI_TalonSRX(2)
        self.motor3 = ctre.WPI_TalonSRX(9)
        self.motor4 = ctre.WPI_TalonSRX(10)

        #Intake Motors
        self.stage1Left = ctre.WPI_TalonSRX(5)
        self.stage1Right = ctre.WPI_TalonSRX(6)
        self.stage2Left = ctre.WPI_TalonSRX(4)
        self.stage2Right = ctre.WPI_TalonSRX(7)
        self.stage3Left = ctre.WPI_TalonSRX(3)
        self.stage3Right = ctre.WPI_TalonSRX(8)

        #Pan Arm Controls
        self.leftPanArm = wpilib.PWMVictorSPX(1)
        self.rightPanArm = wpilib.PWMVictorSPX(4)

        #Shifters
        self.shifter = wpilib.DoubleSolenoid(1,2)
        
        #User Inputs
        self.xboxController = wpilib.XboxController(0)
        #self.playerTwo = wpilib.XboxController(1)
        
        #Setup Logic
        self.rightDriveMotors = wpilib.SpeedControllerGroup(self.motor3,self.motor4)
        self.leftDriveMotors = wpilib.SpeedControllerGroup(self.motor1,self.motor2)
        self.robotDrive = DifferentialDrive(self.leftDriveMotors, self.rightDriveMotors)
        self.rightIntakeMotors = wpilib.SpeedControllerGroup(self.stage1Right, self.stage2Right, self.stage3Right)
        self.leftIntakeMotors = wpilib.SpeedControllerGroup(self.stage1Left, self.stage2Left, self.stage3Left)

        if wpilib.SolenoidBase.getPCMSolenoidVoltageStickyFault(0) == True:
            clearAllPCMStickyFaults(0)

        #Auto mode variables
        self.components = {
            'drive': self.robotDrive
        }
        self.automodes = AutonomousModeSelector('autonomous', self.components)

    def autonomousPeriodic(self):

        #Hud Data Update
        self.statUpdater.UpdateMatchTime()
        self.statUpdater.UpdateBatteryStatus()
        
        #Run auto modes
        self.automodes.run()

    def teleopPeriodic(self):

        #Drive
        self.robotDrive.arcadeDrive(self.xboxController.getX(0), self.xboxController.getY(0))

        #Intake
        self.rightIntakeMotors.set(self.xboxController.getY(1))
        self.leftIntakeMotors.set(self.xboxController.getY(1))
        
        #Pan Arms
        if self.xboxController.getBumperPressed(0):
            self.leftPanArm.set(.75)
        elif self.xboxController.getTriggerAxis(0) >= 0.0:
            self.leftPanArm.set(-.75 * self.xboxController.getTriggerAxis(0))
        if self.xboxController.getBumperPressed(1):
            self.rightPanArm.set(-.75)
        elif self.xboxController.getTriggerAxis(1) <= 0.05:
            self.rightPanArm.set(.75 * self.xboxController.getTriggerAxis(1))

        #Shifting
        if self.xboxController.getAButtonPressed():
            self.shifter.set(wpilib.DoubleSolenoid.Value.kForward)
        if self.xboxController.getBButtonPressed():
            self.shifter.set(wpilib.DoubleSolenoid.Value.kReverse)

if __name__ == "__main__":
    wpilib.run(MyRobot)
