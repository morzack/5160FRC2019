from wpilib.command import CommandGroup

from commands import driveForwards, shootIntake, turnRobot

import wpilib

import robotmap

class PassAutoLineShoot(CommandGroup):
    def __init__(self, robot):
        super().__init__()
        self.addSequential(driveForwards.DriveForward(robot, 160))
        self.addSequential(shootIntake.ShootIntake(robot, 2))
        self.addSequential(shootIntake.ShootIntake(robot, 1))