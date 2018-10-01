from wpilib.command import CommandGroup

from commands import driveForwards, turnRobot, shootIntake

import robotmap

import math

INITIALDISTANCE = 80
TURNANGLE = 15

class CenterDodgeRight(CommandGroup):
    def __init__(self, robot):
        super().__init__()
        # go forwards, turn to the right (positive), go forwards again
        self.addSequential(driveForwards.DriveForward(robot, INITIALDISTANCE))
        self.addSequential(turnRobot.TurnRobot(robot, 0, reset=False))
        self.addSequential(turnRobot.TurnRobot(robot, TURNANGLE))
        self.addSequential(driveForwards.DriveForward(robot, (160-INITIALDISTANCE)/math.cos(math.radians(TURNANGLE))))
        self.addSequential(shootIntake.ShootIntake(robot, 2))
        self.addSequential(shootIntake.ShootIntake(robot, 1))

class CenterDodgeLeft(CommandGroup):
    def __init__(self, robot):
        super().__init__()
        # go forwards, turn to the right (positive), go forwards again
        self.addSequential(driveForwards.DriveForward(robot, INITIALDISTANCE))
        self.addSequential(turnRobot.TurnRobot(robot, 0, reset=False))
        self.addSequential(turnRobot.TurnRobot(robot, TURNANGLE))
        self.addSequential(driveForwards.DriveForward(robot, (160-INITIALDISTANCE)/math.cos(math.radians(-TURNANGLE))))
        self.addSequential(shootIntake.ShootIntake(robot, 2))
        self.addSequential(shootIntake.ShootIntake(robot, 1))

class CenterDodge(CommandGroup):
    def __init__(self, robot):
        super().__init__()
        # go forwards, turn to the right (positive), go forwards again
        self.addSequential(driveForwards.DriveForward(robot, INITIALDISTANCE))
        self.addSequential(turnRobot.TurnRobot(robot, 0, reset=False))
        self.addSequential(turnRobot.TurnRobot(robot, TURNANGLE))
        self.addSequential(driveForwards.DriveForward(robot, (160-INITIALDISTANCE)/math.cos(math.radians(-TURNANGLE))))