'''
#!/usr/bin/env python3
import wpilib

class Drive(object):

# Got to put all drive related information here for futher use


    def __init__(self, robotDrive, xboxController, navx):

        self.xboxController = xboxController
        self.robotDrive = robotDrive
        self.gyro = navx
    
    
        kP = 0.01
        kI = 0.0001
        
        turnController = wpilib.PIDController(kP, kI, 0, 0, self.gyro, output=self.blackbox)
        turnController.setInputRange(-180.0,  180.0)
        turnController.setOutputRange(-.5, .5)
        turnController.setContinuous(True)
        self.turnController = turnController

    
    
  
    
    
    def getYaw(self):
        return self.gyro.getYaw()

    def customDrive(self, posX, posY, posT, mode): #current positions, X, Y, and Throttle
       
        if self.turnController.isEnable() and not self.turnController.onTarget():
            goRotation = self.rotate180
        else:
            self.pidEnable(False)
            goRotation = posX
       
        if mode:
            self.robotDrive.arcadeDrive(goRotation, posY, True)
     #   else:
      #      self.robotDrive.tankDrive(self.xboxController.getRawAxis(5), posY, True)

            
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

    def pidEnable(self, isEnable):
        if isEnable:
            self.turnController.enable()
        else:
            self.turnController.disable()


DRIVE.py is INCOMPLETE
'''

