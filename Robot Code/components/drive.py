#!/usr/bin/env python3
import wpilib
import pathfinder as pf

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

    '''
    def generatePath(self):
        points = [pf.Waypoint(0.0, 0.0, 0.0), pf.Waypoint(10.0, 0.0, 0.0)]

        info, self.trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC, pf.SAMPLES_HIGH, .05, 11.0, 18.0, 60.0)

    def configurationSetup(self):

        modifier = pf.modifiers.TankModifier(trajectory).modify(1.96)

        left = modifier.getLeftTrajectory()
        right = modifier.getRightTrajectory()

        self.left_follower = pf.followers.EncoderFollower(left)
        self.right_follower = pf.followers.EncoderFollower(right)

        self.left_follower.configureEncoder(0, 11243, .5)
        self.right_follower.configureEncoder(0, 13346, .5)
        
        self.left_follower.configurePIDVA(1.0, 0.0, 0.0, 1.0, 0)
        self.right_follower.configurePIDVA(1.0, 0.0, 0.0, 1.0, 0)

    def calculate(side):
        if side=='r':
            a = self.right_follower.calculate(self.rEncoder.getQuadraturePosition())
            print (a)
            print (self.right_follower.getSegment())
            return a
        elif side=='l':
            return self.right_follower.calculate(self.lEncoder.getQuadraturePosition())
        
    def autoTankDrive(self):

        self.robotDrive.tankDrive(self.calculate('l'), self.calculate('r'))
    '''

    def getYaw(self):
        return self.gyro.getYaw()

    def driveMeBoi(self, posX, posY): #current positions, X, Y
        #print (self.gearbox)
        self.funcShifter()
        if self.turnController.isEnabled() and not self.turnController.onTarget():
            goRotation = self.rotate180
        else:
            self.pidEnabled(False)
            goRotation = posX
    
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

    def autonomousDriveForward(self, moveX, moveY, distance):
        self.driveMeBoi(moveX, MoveY)
        if self.lEncoder.getQuadraturePosition() > 8375 * distance:
            self.driveMeBoi(0, 0)
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



