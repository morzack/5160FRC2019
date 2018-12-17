from wpilib.command import CommandGroup

from commands import driveForwards, shootIntake

import robotmap

import pathfinder as pf
import wpilib

class PassAutoLine(CommandGroup):
    MAXVELOCITY = 3
    MAXACCELERATION = 2

    def __init__(self, robot):
        super().__init__()
        points = [pf.Waypoint(0, 0, 0), pf.Waypoint(13, 0, 0)]
        
        info, trajectory = pf.generate(
            points,
            pf.FIT_HERMITE_CUBIC,
            pf.SAMPLES_HIGH,
            max_velocity=PassAutoLine.MAXVELOCITY,
            max_acceleration=PassAutoLine.MAXACCELERATION,
            max_jerk=120.0,
        )

        # Wheelbase Width = 2 ft
        modifier = pf.modifiers.TankModifier(trajectory).modify(robotmap.robotDiameter/12)

        # Do something with the new Trajectories...
        left = modifier.getLeftTrajectory()
        right = modifier.getRightTrajectory()

        leftFollower = pf.followers.EncoderFollower(left)
        leftFollower.configureEncoder(
            robot.drivetrain.encoderLeft, robotmap.encoderPerRev, robotmap.wheelDiameter
        )
        leftFollower.configurePIDVA(1.0, 0.0, 0.0, 1 / PassAutoLine.MAXVELOCITY, 0)

        rightFollower = pf.followers.EncoderFollower(right)
        rightFollower.configureEncoder(
            robot.drivetrain.encoderRight, robotmap.encoderPerRev, robotmap.wheelDiameter
        )
        rightFollower.configurePIDVA(1.0, 0.0, 0.0, 1 / PassAutoLine.MAXVELOCITY, 0)

        self.leftFollower = leftFollower
        self.rightFollower = rightFollower
        
        
        self.addSequential(driveForwards.DriveForward(robot, 160))