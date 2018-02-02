#!/usr/bin/env python3
import wpilib
import pathfinder as pf
from wpilib.drive import DifferentialDrive
import wpilib.drive
import math

class MyRobot(wpilib.IterativeRobot):


    def robotInit(self):


        #Motors
        self.leftMotorInput = wpilib.Talon(1)
        self.rightMotorInput = wpilib.Talon(2)

        self.drive = wpilib.drive.DifferentialDrive(self.leftMotorInput, self.rightMotorInput)


        #Inputs
        self.controller = wpilib.Joystick(0)


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

        self.left_follower = pf.followers.DistanceFollower(left)
        self.right_follower = pf.followers.DistanceFollower(right)

        #self.left_follower.configureEncoder(2, 1000, 5.75)
        self.left_follower.configurePIDVA(5.0, 0.0, 0.0, 1 / 20, 0)

        #self.right_follower.configureEncoder(2, 1000, 5.75)
        self.right_follower.configurePIDVA(5.0, 0.0, 0.0, 1 / 20, 0)

        # simulating an encoder position ticks
        self.counter = 1

    def teleopPeriodic(self):

        self.counter+=1
        print (self.left_follower.calculate(self.counter))

        self.drive.tankDrive(self.controller.getY(), self.controller.getRawAxis(5))


if __name__ == "__main__":
    wpilib.run(MyRobot)
