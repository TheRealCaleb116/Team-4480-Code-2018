#!/usr/bin/env python3
import wpilib

class Intake(object):

    def __init__(self, lowerIntakeMotors, stage3, leftPanArm, rightPanArm):

        self.lowerIntakeMotors = lowerIntakeMotors
        self.stage3 = stage3
        self.leftPanArm = leftPanArm
        self.rightPanArm = rightPanArm

    def suck(self, iSpeed):
        self.lowerIntakeMotors.set(iSpeed ** 3)

    def ohShootDere(self, Output, Input):
        self.stage3.set((Output + Input * -1))

    def panArms(self, leftPanArmPos, rightPanArmPos, mode):
        if mode == True:
            self.leftPanArm.set(leftPanArmPos)
            self.rightPanArm.set(rightPanArmPos)
        else:
            self.leftPanArm.set(leftPanArmPos)
            self.rightPanArm.set(leftPanArmPos)

