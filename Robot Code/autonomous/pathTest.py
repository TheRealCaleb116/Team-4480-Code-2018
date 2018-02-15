from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state
import time
class DriveForward(StatefulAutonomous):

    MODE_NAME = 'PathFinder'
    DEFAULT = True

    def initialize(self):
        self.counter = 0
        self.total = 0
        self.drive.generatePath(0.0, 0.0, 0, 20.0, 10.0, 0)
        self.drive.configurationSetup()
    @timed_state(duration=2.0, next_state='drive_forward', first=True)
    def drive_wait(self):
        self.drive.resetGyro()
        self.drive.driveMeBoi(0, 0)


    @timed_state(duration=10, next_state='stop')
    def drive_forward(self):

        self.drive.autoTankDrive()



    @state()
    def stop(self):
        self.drive.pidEnabled(False)
        self.drive.driveMeBoi(0, 0)
