from wpilib.command import TimedCommand
from systems import subsystems

class IntakeOut(TimedCommand):
    def __init__(self, power, timeoutInSeconds):
        super().__init__('shoot intake at %d power' % power, timeoutInSeconds)

        self.power = power
        self.requires(subsystems.inT)

    def initialize(self):
        subsystems.inT.outTake(self.power)
    
    def end(self):
        subsystems.inT.inTake(0)

class IntakeIn(TimedCommand):
    def __init__(self, power, timeoutInSeconds):
        super().__init__('intake with intake at %d power' % power, timeoutInSeconds)

        self.power = power
        self.requires(subsystems.inT)

    def initialize(self):
        subsystems.inT.inTake(self.power)
    
    def end(self):
        subsystems.inT.inTake(0)