from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state

import wpilib

class DriveForward(StatefulAutonomous):

    DEFAULT = False
    MODE_NAME = 'Left Forward Score (No Turning)'

    def initialize(self):
        self.drive.setAutoSetpoint(909.25*8*12)
        self.drive.resetEncoders()

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
        self.drive.driveMeBoi(0, 0)
        self.drive.gearbox = True
        self.drive.setPoint(self.drive.getYaw())
        if not wpilib.RobotBase.isSimulation():
            self.message = \
                wpilib.DriverStation.getInstance().getGameSpecificMessage()
        else:
            self.message = "R"

    @timed_state(duration=3, next_state='waitForCoast')
    def drive_forward(self):
        self.drive.autoForward.enable()
        self.drive.turnController.enable()
        self.drive.driveMeBoi(0, 0)
        if not self.drive.autoForward.isEnabled():
            self.next_state('waitForCoast')

    @timed_state(duration=1, next_state='decision')
    def waitForCoast(self):
        self.drive.driveMeBoi(0, 0)

    @timed_state(duration=0.5, next_state='stop')
    def decision(self):
        if self.message[0].upper() == 'L':
            self.next_state('ohShootDere')
        else:
            self.next_state('stop')

    @timed_state(duration=0.75, next_state='stop')
    def ohShootDere(self):
        self.drive.driveMeBoi(0, 0)
        self.intake.ohShootDere(1, 0)

    @state()
    def stop(self):
         self.drive.driveMeBoi(0, 0)
         self.intake.ohShootDere(0, 0)
