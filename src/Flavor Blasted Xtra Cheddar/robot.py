#!/usr/bin/env python3

import wpilib
import wpilib.drive
from OI import *


class Robot(wpilib.IterativeRobot):
    
    # motor ports
    # DRIVETRAIN
    frontLeftPort = 14
    backLeftPort = 13
    frontRightPort = 1
    backRightPort = 2

    def robotInit(self):
        # assign motors to object
        self.motorLeftFront = wpilib.PWMTalonSRX(Robot.frontLeftPort)
        self.motorLeftBack = wpilib.PWMTalonSRX(Robot.backLeftPort)
        self.motorRightFront =  wpilib.PWMTalonSRX(Robot.frontRightPort)
        self.motorRightBack = wpilib.PWMTalonSRX(Robot.backRightPort)
        # create a drivetrain ovject to access motors easier
        self.drivetrain = wpilib.drive.MecanumDrive(self.motorLeftFront, self.motorLeftBack, self.motorRightFront, self.motorRightBack)
        # set up a timer to allow for cheap drive by time auto
        self.timer = wpilib.Timer()
        # initialize OI systems for the robot 
        self.OI = OI()

    def autonomousInit(self):
        # this runs before the autonomous
        # reset timer for auto
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        # just dont do anything for autonomous
        # iirc this method is called repeatedly
        if self.timer.accumulatedTime < 2.0:
            self.drivetrain.driveCartesian(0.5, 0, 0)
        else:
            self.drivetrain.driveCartesian(0, 0, 0)  # Stop robot

    def teleopPeriodic(self):
        # teleop method, called repeatedly
        # make OI do special input things
        self.OI.handleInput()
        # move the mecanum DT w/ OI modifiers
        self.drivetrain.driveCartesian(self.OI.handleNumber(self.OI.joystick0.getY()),
                                        self.OI.handleNumber(self.OI.joystick0.getX()), 
                                        self.OI.joystick0.getTwist()+self.OI.joystick0.getAxis(4))

# this is NEEDED because threads are a thing
# you dont want like 5 robot code instnaces, right?
if __name__ == "__main__":
    wpilib.run(Robot)