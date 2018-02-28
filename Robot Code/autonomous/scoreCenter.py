#!/usr/bin/python
# -*- coding: utf-8 -*-
from robotpy_ext.autonomous import StatefulAutonomous, timed_state, \
    state

import wpilib

class CenterScoreAnywhere(StatefulAutonomous):

    MODE_NAME = 'CenterScoreAnywhere'
    DEFAULT = False

    def initialize(self):
        pass

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        self.drive.resetGyro()
        self.drive.resetEncoders()
        self.drive.driveMeBoi(0, 0)
        self.drive.setAutoSetpoint(100500)
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
        self.drive.setAutoSetpoint(50000)
        if self.message[0].upper() == 'L':
            self.drive.setAutoTurn(-90)
            self.next_state('turn')
        elif self.message[0].upper() == 'R':
            self.drive.setAutoTurn(90)
            self.next_state('turn')
        else:
            print ('I did something wrong')

    @timed_state(duration=4, next_state='stop')
    def turn(self):
        self.drive.autoTurn.enable()
        self.drive.driveMeBoi(0, 0)
        if not self.drive.autoTurn.isEnabled():
            self.drive.resetEncoders()
            self.drive.setAutoSetpoint(100000)
            self.next_state('approachSwitch')

    @timed_state(duration=3, next_state='stop')
    def approachSwitch(self):
        self.drive.autoForward.enable()
        self.drive.driveMeBoi(0,0)
        if not self.drive.autoForward.isEnabled():
            self.next_state('ohShootDere')

    @timed_state(duration=3, next_state='stop')
    def ohShootDere(self):
        self.intake.ohShootDere(1, 0)

    @state()
    def stop(self):
        self.intake.ohShootDere(0, 0)
        self.drive.driveMeBoi(0, 0)
