from wpilib.command import CommandGroup

from commands import driveForwards, shootIntake

import robotmap

import fieldConstants

class PassAutoLine(CommandGroup):
    def __init__(self, robot):
        super().__init__()
        self.addSequential(driveForwards.DriveForward(robot, fieldConstants.autoLine))