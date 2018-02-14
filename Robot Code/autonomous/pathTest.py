from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state

class DriveForward(StatefulAutonomous):

    MODE_NAME = 'PathFinder'
    DEFAULT = False
    
    def initialize(self):
        pass
    
    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
         self.drive.driveMeBoi(0, 0)

    
    @timed_state(duration=10, next_state='stop')
    def drive_forward(self):
         self.drive.autoTankDrive()

    @state()
    def stop(self):
         self.drive.driveMeBoi(0, 0)

