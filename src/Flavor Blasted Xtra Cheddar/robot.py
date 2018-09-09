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
        # invert motors
        self.motorLeftFront.setInverted(True)
        self.motorLeftBack.setInverted(True)
        # make motor groups
        self.leftMotors = wpilib.SpeedControllerGroup(self.motorLeftBack, self.motorLeftFront)
        self.rightMotors = wpilib.SpeedControllerGroup(self.motorRightBack, self.motorRightFront)
        # create a drivetrain ovject to access motors easier
        self.drivetrain = wpilib.drive.DifferentialDrive(self.leftMotors, self.rightMotors)
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
        # this method is called repeatedly
        if self.timer.get() < 2.0:
            self.drivetrain.tankDrive(-0.5, -0.5)
        else:
            self.drivetrain.tankDrive(0, 0)  # Stop robot
        self.motorLeftBack.set
    
    def teleopInit(self):
        # teleop period initialization
        pass

    def teleopPeriodic(self):
        # teleop method, called repeatedly
        # make OI do special input things
        self.OI.handleInput()
        # move the mecanum DT w/ OI modifiers
        self.drivetrain.tankDrive(self.OI.handleNumber(self.OI.joystick0.getY(wpilib.XboxController.Hand.kLeft)),
                                        self.OI.handleNumber(self.OI.joystick0.getY(wpilib.XboxController.Hand.kRight)))
    
# this is NEEDED because threads are a thing
# you dont want like 5 robot code instnaces, right?
if __name__ == "__main__":
    wpilib.run(Robot)