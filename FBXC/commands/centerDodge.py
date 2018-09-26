from wpilib.command import CommandGroup

from commands import driveForwards, turnRobot

import math

class CenterDodge(CommandGroup):
    def __init__(self, robot):
        super().__init__()
        # go forwards, turn, go forwards again
        initialDistance = 80
        turnAngle = 5
        self.addSequential(driveForwards.DriveForward(robot, initialDistance))
        self.addSequential(turnRobot.TurnRobot(robot, turnAngle))
        self.addSequential(driveForwards.DriveForward(robot, (144-initialDistance)/math.cos(math.radians(turnAngle))))