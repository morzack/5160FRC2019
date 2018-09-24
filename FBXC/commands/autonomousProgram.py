from wpilib.command.commandgroup import CommandGroup
from wpilib.command.waitcommand import WaitCommand

from commands import moveDrivetrain
from commands import operateIntake

class AutoProgram(CommandGroup):
    def __init__(self):
        super().__init__('Auto Program')

        self.addSequential(moveDrivetrain.MoveDrivetrain(12, 10)) # move to switch for 10s
        self.addSequential(moveDrivetrain.TurnDrivetrain(90, 5))
        self.addSequential(WaitCommand(timeout=1))
        self.addSequential(operateIntake.IntakeOut(0.8, 3)) # shoot cube