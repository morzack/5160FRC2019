from wpilib.command.commandgroup import CommandGroup
from wpilib.command.waitcommand import WaitCommand

import moveDrivetrain

class AutoProgram(CommandGroup):
    def __init__(self):
        super().__init__('Auto Program')

        self.addSequential(moveDrivetrain.MoveDrivetrain(12, 5))
        self.addSequential(WaitCommand(timeout=1))
        self.addSequential(moveDrivetrain.MoveDrivetrain(-12, 5))