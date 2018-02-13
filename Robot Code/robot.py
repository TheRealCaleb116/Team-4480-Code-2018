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
from components import drive, intake
import time

class MyRobot(wpilib.IterativeRobot):

    def disabledInit(self):

        #Update Allience
        self.statUpdater.getAlliance()

        #Send Data to Networktable
        self.statUpdater.UpdateStatus(0)
        self.statUpdater.UpdateMatchTime()

    def autonomousInit(self):

        self.motor1.setNeutralMode(2)
        self.motor2.setNeutralMode(2)
        self.motor3.setNeutralMode(2)
        self.motor4.setNeutralMode(2)

        self.statUpdater.UpdateStatus(1)
        self.statUpdater.UpdateMatchTime()
        self.drive.resetEncoders()

    def teleopInit(self):
        self.statUpdater.UpdateStatus(2)
        self.statUpdater.UpdateMatchTime()
        self.start=None
        self.drive.resetEncoders()

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
        self.leftPanArm = wpilib.PWMVictorSPX(0)
        self.rightPanArm = wpilib.PWMVictorSPX(1)

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
        self.lowerIntakeMotors = wpilib.SpeedControllerGroup(self.stage1Left, self.stage1Right, self.stage2Left, self.stage2Right)
        self.stage3 = wpilib.SpeedControllerGroup(self.stage3Left, self.stage3Right)
        if wpilib.SolenoidBase.getPCMSolenoidVoltageStickyFault(0) == True:
            wpilib.SolenoidBase.clearAllPCMStickyFaults(0)

        #Drive.py init
        self.drive = drive.Drive(self.robotDrive, self.navx, self.motor1, self.motor4, self.shifter)

        #Intake.py
        self.intake = intake.Intake(self.lowerIntakeMotors, self.stage3, self.leftPanArm, self.rightPanArm)

        self.driverStation = wpilib.DriverStation.getInstance()

        #Auto mode variables
        self.components = {
            'drive': self.drive,
            'intake': self.intake
        }
        self.automodes = AutonomousModeSelector('autonomous', self.components)

    def autonomousPeriodic(self):
        self.starter = time.time()
        #Hud Data Update
        self.statUpdater.UpdateMatchTime()
        self.statUpdater.UpdateBatteryStatus()

        #Run auto modes
        self.automodes.run()

        print(time.time()-self.starter)

    def teleopPeriodic(self):

        print (self.driverStation.getGameSpecificMessage())

        #Intake
        self.intake.suck(self.playerTwo.getTriggerAxis(1) + self.playerTwo.getTriggerAxis(0) * -1)

        self.intake.ohShootDere(self.playerTwo.getYButton(), self.playerTwo.getAButton())
        #Pan Arms
        self.intake.panArms(self.playerTwo.getX(0), self.playerTwo.getX(1), not self.playerTwo.getStickButton(0))

        #Drive
        self.drive.driveMeBoi(self.playerOne.getX(0), self.playerOne.getY(0))

        # 11 fps

        if self.playerOne.getXButtonPressed():
            if self.start == None:
                self.start = time.time()
                self.startTics = self.drive.getEncoders()[0]
            else:
                print ((((self.drive.getEncoders()[0]-self.startTics)/11243)/((time.time()-self.start)**2)))
                print ((((self.drive.getEncoders()[0]-self.startTics)/13346)/((time.time()-self.start)**2)))

        #Shifting
        if self.playerOne.getAButton():
            self.drive.gearbox = True
        elif self.playerOne.getBButton():
            self.drive.gearbox = False

        #print (self.drive.getEncoders())

if __name__ == "__main__":
    wpilib.run(MyRobot)
