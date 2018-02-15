#!/usr/bin/env python3
import wpilib
import pathfinder as pf
import math


class Drive(object):

    def __init__(self, robotDrive, navx, lEncoder, rEncoder, shifter):

        self.lEncoder = lEncoder
        self.rEncoder = rEncoder
        self.robotDrive = robotDrive
        self.gyro = navx
        self.shifter = shifter
        self.gearbox = False
        kP = 0.01
        kI = 0.0001

        turnController = wpilib.PIDController(kP, kI, 0, 0, self.gyro, output=self.blackbox)
        turnController.setInputRange(-180.0,  180.0)
        turnController.setOutputRange(-.5, .5)
        turnController.setContinuous(True)
        self.turnController = turnController


        self.generatePath()

        self.configurationSetup()

    def resetPath(self):
        self.left_follower.reset()
        self.right_follower.reset()

        print ("resetted!!!")

    def generatePath(self):
        points = [pf.Waypoint(0.0, 0.0, math.radians(0)), pf.Waypoint(20.0, -10.0, math.radians(0))]

        info, self.trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC, pf.SAMPLES_HIGH, .01, 17.0, 32.0, 60.0)

    def configurationSetup(self):

        modifier = pf.modifiers.TankModifier(self.trajectory).modify(1.96)

        left = modifier.getLeftTrajectory()
        right = modifier.getRightTrajectory()

        self.left_follower = pf.followers.EncoderFollower(left)
        self.right_follower = pf.followers.EncoderFollower(right)

        self.left_follower.configureEncoder(0, 1024, .5)
        self.right_follower.configureEncoder(0, 1024, .5)

        self.left_follower.configurePIDVA(.8, 0.0, 0.0, 1.0/17.0, 0)
        self.right_follower.configurePIDVA(.8, 0.0, 0.0, 1.0/17.0, 0)

        #print (self.trajectory)

    def calculate(self):
        r = -1*self.right_follower.calculate(self.rEncoder.getQuadraturePosition())
        l = self.left_follower.calculate(self.lEncoder.getQuadraturePosition())
        if not self.right_follower.isFinished():
            currentAngle = self.getYaw()
            print (currentAngle)
            desiredAngle = math.degrees(self.left_follower.getHeading())

            #print (math.degrees(self.left_follower.getHeading()))

            angleDifference = self.boundHalfDegrees(desiredAngle - currentAngle)


            angle = .8*(-1.0/80.0)*angleDifference

            print (currentAngle," calculated:",angle, " left:", l, " right:", r)


            return ((l+angle), (r-angle))
        else:
            return (0, 0)

    def boundHalfDegrees(self, angle_degrees):
        while angle_degrees >=180.0:
            angle_degrees -= 360.0

        while angle_degrees < -180.0:
            angle_degrees += 360.0

        return angle_degrees

    def resetGyro(self):
        self.gyro.zeroYaw()

    def autoTankDrive(self):
        l, r = self.calculate()
        self.robotDrive.tankDrive(l, r)


    def getYaw(self):
        return self.gyro.getYaw()

    def driveMeBoi(self, posX, posY): #current positions, X, Y
        self.funcShifter()
        if self.turnController.isEnabled() and not self.turnController.onTarget():
            goRotation = self.rotate180
        else:
            self.pidEnabled(False)
            goRotation = posX

        self.robotDrive.arcadeDrive(goRotation * -1, posY, True)


        self.robotDrive.arcadeDrive(goRotation * -1, posY, True)

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
        return (self.lEncoder.getQuadraturePosition(), self.rEncoder.getQuadraturePosition())


    def funcShifter(self):
        if self.gearbox == True:
            self.shifter.set(wpilib.DoubleSolenoid.Value.kForward)
        elif self.gearbox == False:
            self.shifter.set(wpilib.DoubleSolenoid.Value.kReverse)
