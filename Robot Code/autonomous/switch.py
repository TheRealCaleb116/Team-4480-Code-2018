from robotpy_ext.autonomous import StatefulAutonomous, timed_state, state

class Switch(StatefulAutonomous):

    DEFAULT = True
    MODE_NAME = 'Switch'
    
    def initialize(self):
        pass
    
    @timed_state(duration=0.5, next_state='drive_forward', first=True)
    def drive_wait(self):
         self.drive.driveMeBoi(0, 0)
    
    @timed_state(duration=1.5, next_state='stop')
    def drive_forward(self):
        if self.drive.getEncoders() > (10 * 11000, 10 * 13000):
            self.drive.driveMeBoi(0, -.5)


    @state()
    def stop(self):
         self.drive.driveMeBoi(0, 0)

