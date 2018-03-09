from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state

class DriveForward(StatefulAutonomous):

    DEFAULT = False
    MODE_NAME = 'Drive Forward'
    
    def initialize(self):
        self.drive.setAutoSetpoint(909.25*12.5*12) # old 696.75

    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
         self.drive.driveMeBoi(0, 0)
         self.drive.resetEncoders()

    @timed_state(duration=1.5, next_state='stop')
    def drive_forward(self):
        self.drive.autoForward.enable()
        self.drive.driveMeBoi(0, 0)
        if not self.drive.autoForward.isEnabled():
            self.next_state('stop')

    @state()
    def stop(self):
         self.drive.driveMeBoi(0, 0)
