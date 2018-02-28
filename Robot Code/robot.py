#!/usr/bin/env python3
'''
Python3 Robot code: "Willie" using Robotpy 2018 - 2018, 4480 "Forty48ie" "UC-Botics" out of Upsala, Minnesota
This Code is protected by ROBBY ACT under the leadership of our profound and prominent
Senior Mechanical Engineer: Ethan Robertson
and hereby stands as an inspirations to all of us here to do great things.

~ 696.75 tics per inch

'''

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

#HUD Imports
from components import statusUpdater as SU
from components import drive, intake

class MyRobot(wpilib.IterativeRobot):

    def disabledInit(self):

        #Update Allience
        self.statUpdater.getAlliance()

        #Send Data to Networktable
        self.statUpdater.UpdateStatus(0)
        self.statUpdater.UpdateMatchTime()

    def robotInit(self):

        #Networktables
        self.netTable = NetworkTables.getTable('SmartDashboard')

        #Hud Data Handlers
        self.statUpdater = SU.StatusUpdater(self,self.netTable)

        #Camera Server
        wpilib.CameraServer.launch()

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

        #Climb
        self.pto = wpilib.DoubleSolenoid(3,4)
        self.climbLift = wpilib.Solenoid(5)

        #User Inputs
        self.playerOne = wpilib.XboxController(0)
        self.playerTwo = wpilib.XboxController(1)

        #Navx
        self.navx = navx.AHRS.create_spi()

        #Auto Path Setup

        #User Inputs
        self.playerOne = wpilib.XboxController(0)
        self.playerTwo = wpilib.XboxController(1)

        #Navx
        self.navx = navx.AHRS.create_spi()

        #Points
        #self.points = []

        #Setup Logic
        self.rightDriveMotors = wpilib.SpeedControllerGroup(self.motor3,self.motor4)

        #Hud DataHandlers
        self.statUpdater = SU.StatusUpdater(self,self.netTable)

        self.leftDriveMotors = wpilib.SpeedControllerGroup(self.motor1,self.motor2)

        self.leftDriveMotors.setInverted(True)

        self.robotDrive = DifferentialDrive(self.leftDriveMotors, self.rightDriveMotors)

        self.lowerIntakeMotors = wpilib.SpeedControllerGroup(self.stage1Left, self.stage1Right, self.stage2Left, self.stage2Right)

        self.stage3 = wpilib.SpeedControllerGroup(self.stage3Left, self.stage3Right)

        if wpilib.SolenoidBase.getPCMSolenoidVoltageStickyFault(0) == True:
            wpilib.SolenoidBase.clearAllPCMStickyFaults(0)

        self.pto.set(wpilib.DoubleSolenoid.Value.kReverse)

        #Drive.py init
        self.drive = drive.Drive(self.robotDrive, self.navx, self.motor1, self.motor2, self.motor3, self.motor4, self.shifter)

        #Intake.py
        self.intake = intake.Intake(self.lowerIntakeMotors, self.stage3, self.leftPanArm, self.rightPanArm)

        #Driver Station Instance
        self.driverStation = wpilib.DriverStation.getInstance()

        #Auto mode variables
        self.components = {
            'drive': self.drive,
            'intake': self.intake
        }
        self.automodes = AutonomousModeSelector('autonomous', self.components)

    def autonomousInit(self):

        self.motor1.setNeutralMode(2)
        self.motor2.setNeutralMode(2)
        self.motor3.setNeutralMode(2)
        self.motor4.setNeutralMode(2)

        self.statUpdater.UpdateStatus(1)
        self.statUpdater.UpdateMatchTime()
        self.drive.resetEncoders()

        self.drive.gearbox = True


    def autonomousPeriodic(self):
        #Hud Data Update
        self.statUpdater.UpdateMatchTime()
        self.statUpdater.UpdateBatteryStatus()

        self.automodes.run()

    def teleopInit(self):
        self.motor1.setNeutralMode(1)
        self.motor2.setNeutralMode(1)
        self.motor3.setNeutralMode(1)
        self.motor4.setNeutralMode(1)

        self.statUpdater.UpdateStatus(2)
        self.statUpdater.UpdateMatchTime()
        self.start=None
        self.drive.resetEncoders()

        self.statUpdater.UpdateMatchTime()

        self.drive.autoForward.disable()
        self.drive.autoTurn.disable()
        self.drive.turnController.disable()
        self.drive.resetGyro()

    def teleopPeriodic(self):

        mult = 0.5 + (self.playerOne.getTriggerAxis(1) * 0.5)

        #Intake
        self.intake.suck(self.playerTwo.getTriggerAxis(1) + self.playerTwo.getTriggerAxis(0) * -1)
        self.intake.ohShootDere(self.playerTwo.getYButton(), self.playerTwo.getAButton())

        #Data Updaters
        self.statUpdater.UpdateBatteryStatus()
        self.statUpdater.UpdateMatchTime();


        #Pan Arms
        self.intake.panArms(self.playerTwo.getX(0), self.playerTwo.getX(1), not self.playerTwo.getStickButton(0))

        #Drive

        if self.pto.get() == wpilib.DoubleSolenoid.Value.kForward:
            self.robotDrive.tankDrive(self.playerOne.getY(1), self.playerOne.getY(0))
        else:
            self.drive.driveMeBoi(self.playerOne.getX(1) * 0.7, (self.playerOne.getY(0) * mult))

        #Shifting
        if self.playerOne.getAButton():
            self.drive.gearbox = True
        elif self.playerOne.getBButton():
            self.drive.gearbox = False

        #FlipFlip
        if self.playerOne.getBumperPressed(0) == True:
            self.drive.flipflip()

        #Climb Mechanism

        if self.playerOne.getStartButton() == True:
            self.climbLift.set(True)
        elif self.playerOne.getYButton() == True:
            self.pto.set(wpilib.DoubleSolenoid.Value.kForward)
            self.climbLift.set(False)
        elif self.playerOne.getXButton() == True:
            self.pto.set(wpilib.DoubleSolenoid.Value.kReverse)

if __name__ == "__main__":
    wpilib.run(MyRobot)
