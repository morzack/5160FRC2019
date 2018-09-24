from wpilib.command import TimedCommand
from systems import subsystems

class MoveDrivetrain(TimedCommand):
    def __init__(self, distance, timeoutInSeconds):
        super().__init__('move drivetrain %d inches' % distance, timeoutInSeconds)

        self.distance = distance
        self.requires(subsystems.dt)

    def initialize(self):
        subsystems.dt.moveEncoder(self.distance)

class TurnDrivetrain(TimedCommand): # turn using degrees (as a delta)
    def __init__(self, degrees, timeoutInSeconds):
        super().__init__('turn drivetrain %d degrees' % degrees, timeoutInSeconds)

        self.degrees = degrees
        self.requires(subsystems.dt)

    def initialize(self):
        subsystems.dt.turnDegrees(self.degrees)