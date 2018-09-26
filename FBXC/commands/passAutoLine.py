from wpilib.command import CommandGroup

from commands import driveForwards, shootIntake

class PassAutoLine(CommandGroup):
    def __init__(self, robot):
        super().__init__()
        self.addSequential(driveForwards.DriveForward(robot, 120))