from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state

class DriveForward(StatefulAutonomous):

    DEFAULT = False
    MODE_NAME = 'Forward Score'

    def initialize(self):
        self.drive.setAutoSetpoint(696.75*6*12)
        self.drive.resetEncoders()
    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
         self.drive.driveMeBoi(0, 0)
         self.drive.gearbox = True

    @timed_state(duration=3, next_state='waitForCoast')
    def drive_forward(self):
        self.drive.autoForward.enable()
        self.drive.driveMeBoi(0, 0)
        if not self.drive.autoForward.isEnabled():
            self.next_state('waitForCoast')

    @timed_state(duration=1, next_state='ohShootDere')
    def waitForCoast(self):
        self.drive.driveMeBoi(0, 0)

    @timed_state(duration=0.75, next_state='stop')
    def ohShootDere(self):
        self.drive.driveMeBoi(0, 0)
        self.intake.ohShootDere(1, 0)

    @state()
    def stop(self):
         self.drive.driveMeBoi(0, 0)
         self.intake.ohShootDere(0, 0)
