#!/usr/bin/env python3
import wpilib

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

    def getEncoders(self):
        return (self.lEncoder.getQuadratureVelocity(), self.rEncoder.getQuadratureVelocity())

    def funcShifter(self):
        if self.gearbox == True:
            self.shifter.set(wpilib.DoubleSolenoid.Value.kForward)
        elif self.gearbox == False:
            self.shifter.set(wpilib.DoubleSolenoid.Value.kReverse)



