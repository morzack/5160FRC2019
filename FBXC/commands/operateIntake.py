from wpilib.command import TimedCommand
from FBXC.systems import subsystems

class IntakeOut(TimedCommand):
    def __init__(self, power, timeoutInSeconds):
        super().__init__('shoot intake at %d power' % power)

        self.power = power
        self.requires(subsystems.intake)

    def initialize(self):
        subsystems.intake.outTake(self.power)



class IntakeIn(TimedCommand):
    def __init__(self, power, timeoutInSeconds):
        super().__init__('intake with intake at %d power' % power)

        self.power = power
        self.requires(subsystems.intake)

    def initialize(self):
        subsystems.intake.inTake(self.power)