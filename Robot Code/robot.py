#!/usr/bin/env python3
# Python3 Robot code: "Unititled"
# 2018 - 2018, 4480 "Forty48ie" "UC-Botics"
#

import wpilib
import wpilib.buttons
import pathfinder as pf
import random
from robotpy_ext.autonomous import AutonomousModeSelector
from robotpy_ext.common_drivers import units, navx
import networktables
from wpilib.drive import DifferentialDrive
import wpilib.drive
import math
import hal

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


        points = [
            pf.Waypoint(-4, -1, math.radians(-45.0)),
            pf.Waypoint(-2, -2, 0),
            pf.Waypoint(0, 0, 0),
        ]

        info, trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC,
                                       pf.SAMPLES_HIGH, 0.05, 1.7, 2.0, 60.0)

        # Wheelbase Width = 0.5m
        modifier = pf.modifiers.TankModifier(trajectory).modify(0.5)

        # Do something with the new Trajectories...
        left = modifier.getLeftTrajectory()
        right = modifier.getRightTrajectory()
        #Navigation and Logistics

        self.left_follower = pf.followers.EncoderFollower(left)
        self.right_follower = pf.followers.EncoderFollower(right)

        self.left_follower.configureEncoder(2, 1000, 5.75)
        self.left_follower.configurePIDVA(1.0, 0.0, 0.0, 1 / 2.0, 0)

        #Defining Variables
        self.dm = True


        #Auto mode variables
        self.components = {
            'drive': self.drive
        }
        self.automodes = AutonomousModeSelector('autonomous', self.components)


    def autonomousPeriodic(self):
        self.automodes.run()


    def teleopPeriodic(self):
        something = int(self.xboxController.getY()*10)
        print (self.left_follower.calculate(random.randint(1,20)))

        self.drive.tankDrive(self.xboxController.getY(), self.xboxController.getRawAxis(5))


if __name__ == "__main__":
    wpilib.run(MyRobot)
