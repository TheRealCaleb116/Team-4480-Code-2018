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
from components import drive

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
        self.rightPanArm = wpilib.PWMVictorSPX(0)

        #Shifters
        self.shifter = wpilib.DoubleSolenoid(1,2)
        
        #User Inputs
        self.playerOne = wpilib.XboxController(0)
        self.playerTwo = wpilib.XboxController(1)
        
        #Navx
        self.navx = navx.AHRS.create_spi()
        
        #Encoders
        
        
        #Setup Logic
        self.rightDriveMotors = wpilib.SpeedControllerGroup(self.motor3,self.motor4)
        self.leftDriveMotors = wpilib.SpeedControllerGroup(self.motor1,self.motor2)
        self.robotDrive = DifferentialDrive(self.leftDriveMotors, self.rightDriveMotors)
        self.rightLowerIntakeMotors = wpilib.SpeedControllerGroup(self.stage1Right, self.stage2Right)
        self.leftLowerIntakeMotors = wpilib.SpeedControllerGroup(self.stage1Left, self.stage2Left)

        if wpilib.SolenoidBase.getPCMSolenoidVoltageStickyFault(0) == True:
            wpilib.SolenoidBase.clearAllPCMStickyFaults(0)
        
        #Drive.py init
        self.drive = drive.Drive(self.robotDrive, self.navx, self.motor1, self.motor3, self.shifter)
        
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
        
        #Intake
        if self.playerTwo.getTriggerAxis(0):
            self.leftLowerIntakeMotors.set(-1)
            self.rightLowerIntakeMotors.set(1)
        elif self.playerTwo.getTriggerAxis(1):
            self.rightLowerIntakeMotors.set(-1)
            self.leftLowerIntakeMotors.set(1)
        else:
            self.rightLowerIntakeMotors.set(0)
            self.leftLowerIntakeMotors.set(0)
        if self.playerTwo.getAButton():
            self.stage3Left.set(1)
            self.stage3Right.set(-1)
        elif self.playerTwo.getYButton():
            self.stage3Left.set(-1)
            self.stage3Right.set(1)
        else:
            self.stage3Left.set(0)
            self.stage3Right.set(0)
        #Pan Arms
        self.rightPanArm.set(0.5 * self.playerTwo.getX(0))
        self.leftPanArm.set(0.5 * self.playerTwo.getX(1))

        #Drive
        self.drive.driveMeBoi(self.playerOne.getX(0), self.playerOne.getY(0))

        #Shifting
        if self.playerOne.getAButton():
            self.drive.gearbox = True
        elif self.playerOne.getBButton():
            self.drive.gearbox = False

if __name__ == "__main__":
    wpilib.run(MyRobot)
