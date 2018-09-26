from wpilib.command import CommandGroup

from commands import driveForwards, turnRobot

class CenterDodge(CommandGroup):
    def __init__(self, robot):
        super().__init__()
        # go forwards, turn, go forwards again
        self.addSequential(driveForwards.DriveForward(robot, 60))
        self.addSequential(turnRobot.TurnRobot(robot, 45))
        self.addSequential(driveForwards.DriveForward(robot, 84.85))