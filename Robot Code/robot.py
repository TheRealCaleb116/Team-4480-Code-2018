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
        self.playerOne = wpilib.XboxController(0)
        self.playerTwo = wpilib.XboxController(1)
        
        #Setup Logic
        self.rightDriveMotors = wpilib.SpeedControllerGroup(self.motor3,self.motor4)
        self.leftDriveMotors = wpilib.SpeedControllerGroup(self.motor1,self.motor2)
        self.robotDrive = DifferentialDrive(self.leftDriveMotors, self.rightDriveMotors)
        self.rightLowerIntakeMotors = wpilib.SpeedControllerGroup(self.stage1Right, self.stage2Right)
        self.leftLowerIntakeMotors = wpilib.SpeedControllerGroup(self.stage1Left, self.stage2Left)

        if wpilib.SolenoidBase.getPCMSolenoidVoltageStickyFault(0) == True:
            wpilib.SolenoidBase.clearAllPCMStickyFaults(0)

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
        self.robotDrive.curvatureDrive(self.playerOne.getY(0), self.playerOne.getX(1), True)
        
        #self.robotDrive.arcadeDrive(self.playerOne.getX(0), self.playerOne.getY(0))

        #Intake
        if self.playerTwo.getTriggerAxis(0) >= 0.1:
            self.leftLowerIntakeMotors.set(self.playerTwo.getTriggerAxis(0))
            self.rightLowerIntakeMotors.set(self.playerTwo.getTriggerAxis(0))
        if self.playerTwo.getTriggerAxis(1) >= 0.1:
            self.rightLowerIntakeMotors.set(self.playerTwo.getTriggerAxis(1))
            self.leftLowerIntakeMotors.set(self.playerTwo.getTriggerAxis(1))
        self.stage3Left.set(self.playerTwo.getY(0))
        self.stage3Right.set(self.playerTwo.getY(0))

        #Pan Arms
        self.rightPanArm.set(0.5 * self.playerTwo.getX(1))
        self.leftPanArm.set(0.5 * self.playerTwo.getX(0))

        #Shifting
        if self.playerOne.getAButtonPressed():
            self.shifter.set(wpilib.DoubleSolenoid.Value.kForward)
        if self.playerOne.getBButtonPressed():
            self.shifter.set(wpilib.DoubleSolenoid.Value.kReverse)

if __name__ == "__main__":
    wpilib.run(MyRobot)
