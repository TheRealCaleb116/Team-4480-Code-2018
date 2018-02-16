#!/usr/bin/python
# -*- coding: utf-8 -*-

import wpilib
import pathfinder as pf
import math


class Drive(object):

    def __init__(
        self,
        robotDrive,
        navx,
        motor1,
        motor2,
        motor3,
        motor4,
        shifter,
        points,
        ):

        self.lEncoder = motor1
        self.rEncoder = motor4
        self.motor2 = motor2
        self.motor3 = motor3

        self.robotDrive = robotDrive
        self.gyro = navx
        self.shifter = shifter
        self.gearbox = False
        kP = .01
        kI = 0.0001
        self.counter = 10
        turnController = wpilib.PIDController(
            kP,
            kI,
            0,
            0,
            self.gyro,
            output=self.blackbox,
            )
        turnController.setInputRange(-180.0, 180.0)
        turnController.setOutputRange(-.5, .5)
        turnController.setContinuous(True)
        self.turnController = turnController

        # this will for going forward in auto

        autoForwardP = 0.02  # I have no idea if this is good enough

        autoForward = wpilib.PIDController(
            autoForwardP,
            0,
            0,
            0,
            self.getEncoder,
            output=self.autoForwardOutput,
            )
        autoForward.setInputRange(-250000, 250000.0)  # I don't know what to put for the input range
        autoForward.setOutputRange(-1.0, 1.0)
        autoForward.setContinuous(False)
        autoForward.setPercentTolerance(.5)
        self.autoForward = autoForward

        autoP = 0.015

        autoTurn = wpilib.PIDController(
            autoP,
            0,
            0,
            0,
            self.gyro,
            output=self.autoTurnOutput,
            )
        autoTurn.setInputRange(-180.0, 180.0)
        autoTurn.setOutputRange(-.75, .75)
        autoTurn.setContinuous(True)
        autoTurn.setPercentTolerance(1)
        self.autoTurn = autoTurn

    def autoTurnOutput(self, output):
        self.autoTurnVelocity = output

    def setAutoTurn(self, angle):
        self.autoTurn.setSetpoint(angle)

    def getEncoder(self):
        return self.rEncoder.getQuadraturePosition()

    def autoForwardOutput(self, output):
        self.forwardVelocity = output

    def setAutoSetpoint(self, angle):
        self.autoForward.setSetpoint(angle)

    def resetPath(self):
        self.left_follower.reset()
        self.right_follower.reset()

    def generatePath(self):

        # self.points = [pf.Waypoint(startX, startY, math.radians(startRotation)), pf.Waypoint(endX, endY, math.radians(endRotation))]

        (info, self.trajectory) = pf.generate(
            self.points,
            pf.FIT_HERMITE_CUBIC,
            pf.SAMPLES_HIGH,
            .01,
            17.0,
            32.0,
            60.0,
            )

    def configurationSetup(self):
        modifier = \
            pf.modifiers.TankModifier(self.trajectory).modify(1.96)
        left = modifier.getLeftTrajectory()
        right = modifier.getRightTrajectory()

        self.left_follower = pf.followers.EncoderFollower(left)
        self.right_follower = pf.followers.EncoderFollower(right)

        self.left_follower.configureEncoder(0, 1024, .5)
        self.right_follower.configureEncoder(0, 1024, .5)

        self.left_follower.configurePIDVA(.8, 0.0, 0.0, 1.0 / 17.0, 0)
        self.right_follower.configurePIDVA(.8, 0.0, 0.0, 1.0 / 17.0, 0)

        # print (self.trajectory)

    def calculate(self):
        r = -1 \
            * self.right_follower.calculate(self.rEncoder.getQuadraturePosition())
        l = \
            self.left_follower.calculate(self.lEncoder.getQuadraturePosition())
        if not self.right_follower.isFinished():
            currentAngle = self.getYaw()
            print (currentAngle)
            desiredAngle = math.degrees(self.left_follower.getHeading())

            # print (math.degrees(self.left_follower.getHeading()))

            angleDifference = self.boundHalfDegrees(desiredAngle
                    - currentAngle)

            angle = .8 * (-1.0 / 80.0) * angleDifference

            print (
                currentAngle,
                ' calculated:',
                angle,
                ' left:',
                l,
                ' right:',
                r,
                )

            return (l + angle, r - angle)
        else:
            return (0, 0)

    def boundHalfDegrees(self, angle_degrees):
        while angle_degrees >= 180.0:
            angle_degrees -= 360.0
        while angle_degrees < -180.0:
            angle_degrees += 360.0
        return angle_degrees

    def resetGyro(self):
        self.gyro.zeroYaw()

    def autoTankDrive(self):
        (l, r) = self.calculate()
        self.robotDrive.tankDrive(l, r)

    def getYaw(self):
        return self.gyro.getYaw()

    def driveMeBoi(self, posX, posY):  # current positions, X, Y
        self.funcShifter()

        if self.turnController.isEnabled() \
            and not self.turnController.onTarget():
            self.autoForward.disable()
            self.autoTurn.disable()
            self.robotDrive.arcadeDrive(self.rotate180 * -1, posY, True)
        elif self.autoForward.isEnabled() \
            and not self.autoForward.onTarget():

            self.turnController.disable()
            self.autoTurn.disable()
            self.robotDrive.arcadeDrive(0, self.forwardVelocity, False)
        elif self.autoTurn.isEnabled() and not self.autoTurn.onTarget():

            self.turnController.disable()
            self.autoForward.disable()
            self.robotDrive.arcadeDrive(self.autoTurnVelocity, 0, False)
        else:
            self.turnController.disable()
            self.autoForward.disable()
            self.autoTurn.disable()
            self.robotDrive.arcadeDrive(posX * -1, posY, True)

    def blackbox(self, output):
        self.rotate180 = output

    def setPoint(self, angle):
        self.turnController.setSetpoint(angle)

    def flipflip(self):
        currentAngle = self.getYaw()
        if currentAngle >= 0:
            self.setPoint(currentAngle - 180)
        else:
            self.setPoint(currentAngle + 180)

    def pidEnabled(self, isEnabled):
        if isEnabled:
            self.turnController.enable()
        else:
            self.turnController.disable()

    def resetEncoders(self):
        self.lEncoder.setQuadraturePosition(0, 0)
        self.rEncoder.setQuadraturePosition(0, 0)

    def getEncoders(self):
        return (self.lEncoder.getQuadraturePosition(),
                self.rEncoder.getQuadraturePosition())

    def funcShifter(self):
        if self.gearbox == True:
            self.shifter.set(wpilib.DoubleSolenoid.Value.kForward)
        elif self.gearbox == False:
            self.shifter.set(wpilib.DoubleSolenoid.Value.kReverse)
