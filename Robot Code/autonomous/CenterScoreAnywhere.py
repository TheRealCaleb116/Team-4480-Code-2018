#!/usr/bin/python
# -*- coding: utf-8 -*-
from robotpy_ext.autonomous import StatefulAutonomous, timed_state, \
    state

import wpilib

class CenterScoreAnywhere(StatefulAutonomous):

    MODE_NAME = 'CenterScoreAnywhere'
    DEFAULT = True

    def initialize(self):
        pass

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        self.drive.resetGyro()
        self.drive.resetEncoders()
        self.drive.driveMeBoi(0, 0)
        self.drive.setAutoSetpoint(696.75*10.5) #969.75 tics/inch * Feet we want to go * 12 inches to make it feet
        if not wpilib.RobotBase.isSimulation():
            self.message = \
                wpilib.DriverStation.getInstance().getGameSpecificMessage()
        else:
            self.message = "L"

    @timed_state(duration=5, next_state='stop')
    def drive_forward(self):
        self.drive.autoForward.enable()
        self.drive.driveMeBoi(0, 0)
        if not self.drive.autoForward.isEnabled():
            self.next_state('decisionLeftRight')

    @state()
    def decisionLeftRight(self):
        self.drive.setAutoSetpoint(69.75 * 64.5)
        if self.message[0].upper() == 'L':
            self.drive.setAutoTurn(-90)
            self.next_state('turn')
        elif self.message[0].upper() == 'R':
            self.drive.setAutoTurn(90)
            self.next_state('turn')
        else:
            print ('I did something wrong')

    @timed_state(duration=3, next_state='stop')
    def turn(self):
        self.drive.autoTurn.enable()
        self.drive.driveMeBoi(0, 0)
        if not self.drive.autoTurn.isEnabled():
            self.next_state('offSetSwitch')

    @timed_state(duration=5, next_state='stop')
    def offSetSwitch(self):
        self.drive.autoForward.enable()
        self.drive.driveMeBoi(0, 0)
        if not self.drive.autoForward.isEnabled():
            self.drive.resetEncoders()
            self.drive.setAutoSetpoint(696.75*3*12)
            self.drive.resetGyro()
            self.next_state('decisionAgain')
    @state
    def decisionAgain(self):
        if self.message[0].upper() == 'L':
            self.drive.setAutoTurn(90)
            self.next_state('turnAgain')
        elif self.message[0].upper() == 'R':
            self.drive.setAutoTurn(-90)
            self.next_state('turnAgain')
        else:
            print ('I did something wrong')


    @timed_state(duration=4, next_state='stop')
    def turnAgain(self):
        self.drive.autoTurn.enable()
        self.drive.driveMeBoi(0, 0)
        if not self.drive.autoTurn.isEnabled():
            self.drive.resetEncoders()
            self.next_state('approachSwitch')

    @timed_state(duration=3, next_state='stop')
    def approachSwitch(self):
        self.drive.autoForward.enable()
        self.drive.driveMeBoi(0,0)
        if not self.drive.autoForward.isEnabled():
            self.next_state('ohShootDere')

    @timed_state(duration=3, next_state='stop')
    def ohShootDere(self):
        self.drive.driveMeBoi(0,0)
        self.intake.ohShootDere(1, 0)

    @state()
    def stop(self):
        self.intake.ohShootDere(0, 0)
        self.drive.driveMeBoi(0, 0)
