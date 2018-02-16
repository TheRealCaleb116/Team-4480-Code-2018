from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state

class DriveForward(StatefulAutonomous):

    #DEFAULT = True
    MODE_NAME = 'Drive Forward'
    
    def initialize(self):
        pass
    
    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
         self.drive.driveMeBoi(0, 0)
    
    @timed_state(duration=1.5, next_state='stop')
    def drive_forward(self):
         self.drive.driveMeBoi(0, -.5)

    @state()
    def stop(self):
         self.drive.driveMeBoi(0, 0)
