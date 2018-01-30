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


        # pathfinder stuff

        points = [
            pf.Waypoint(-4, -1, math.radians(-45.0)),
            pf.Waypoint(-2, -2, 0),
            pf.Waypoint(0, 0, 0),
        ]

        info, trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC,
                                       pf.SAMPLES_HIGH, 0.05, 1.7, 2.0, 60.0)

        # Wheelbase Width = 0.5m
        modifier = pf.modifiers.TankModifier(trajectory).modify(0.5)

        left = modifier.getLeftTrajectory()
        right = modifier.getRightTrajectory()

        self.left_follower = pf.followers.EncoderFollower(left)
        self.right_follower = pf.followers.EncoderFollower(right)

        self.left_follower.configureEncoder(2, 1000, 5.75)
        self.left_follower.configurePIDVA(1.0, 0.0, 0.0, 1 / 1.7, 0)

        # simulating an encoder position ticks
        self.counter = 100

        self.components = {
            'drive': self.drive
        }
        self.automodes = AutonomousModeSelector('autonomous', self.components)


    def autonomousPeriodic(self):
        self.automodes.run()


    def teleopPeriodic(self):
        self.counter+=100
        print (self.left_follower.calculate(self.counter))

        self.drive.tankDrive(self.xboxController.getY(), self.xboxController.getRawAxis(5))


if __name__ == "__main__":
    wpilib.run(MyRobot)
