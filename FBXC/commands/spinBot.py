from wpilib.command import CommandGroup

from commands import turnRobot, shootIntake

import robotmap

class SpinBot(CommandGroup):
    def __init__(self, robot):
        super().__init__()
        self.addSequential(turnRobot.TurnRobot(robot, 180))