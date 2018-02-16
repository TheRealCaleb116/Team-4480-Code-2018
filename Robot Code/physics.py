#
# See the notes for the other physics sample
#


from pyfrc.physics import drivetrains


class PhysicsEngine(object):
    '''
       Simulates a 4-wheel robot using Tank Drive joystick control
    '''


    def __init__(self, physics_controller):
        '''
            :param physics_controller: `pyfrc.physics.core.Physics` object
                                       to communicate simulation effects to
        '''

        self.physics_controller = physics_controller
        self.physics_controller.add_device_gyro_channel('navxmxp_spi_4_angle')

    def update_sim(self, hal_data, now, tm_diff):
        '''
            Called when the simulation parameters for the program need to be
            updated.

            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        '''

        # Simulate the drivetrain
        lr_motor = hal_data['CAN'][1]['value']
        rr_motor = hal_data['CAN'][9]['value']
        lf_motor = hal_data['CAN'][2]['value']
        rf_motor = hal_data['CAN'][10]['value']

        speed = 5

        # encoders
        l = -(lf_motor + lr_motor) * 0.5 * speed
        r = (rf_motor + rr_motor) * 0.5 * speed
        hal_data['CAN'][1]['quad_position'] += int(l*tm_diff*10240)
        hal_data['CAN'][10]['quad_position'] += int(r*tm_diff*10240)

        speed, rotation = drivetrains.four_motor_drivetrain(lr_motor, rr_motor, lf_motor, rf_motor, speed=speed)
        self.physics_controller.drive(speed, rotation, tm_diff)
