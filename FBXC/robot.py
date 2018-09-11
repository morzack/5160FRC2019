#!/usr/bin/env python3

import wpilib
import wpilib.drive
import ctre
from OI import *
from drivetrain import *


class Robot(wpilib.IterativeRobot):
    motorData = {
        "driveLeftFront"    : {
            "port"          : 2,
            "type"          : "TalonSRX",
            "inverted"      : True
        },
        "driveRightFront"   : {
            "port"          : 13,
            "type"          : "TalonSRX",
            "inverted"      : False
        },
        "driveLeftBack"    : {
            "port"          : 1,
            "type"          : "TalonSRX",
            "inverted"      : True
        },
        "driveRightBack"   : {
            "port"          : 14,
            "type"          : "TalonSRX",
            "inverted"      : False
        },

        "intakeLift"        : {
            "port"          : 11,
            "type"          : "TalonSRX",
            "inverted"      : False
        },
        "intakeLeftArm"     : {
            "port"          : 5,
            "type"          : "TalonSRX",
            "inverted"      : True
        },
        "intakeRightArm"    : {
            "port"          : 10,
            "type"          : "TalonSRX",
            "inverted"      : False
        }
    }

    def robotInit(self):
        # get drivetrain
        self.dt = Drivetrain()

        # misc initializations
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
            self.dt.drivetrain.driveCartesian(0.8, 0, 0)
        else:
            self.dt.drivetrain.driveCartesian(0, 0, 0)  # Stop robot
    
    def teleopInit(self):
        # teleop period initialization
        pass

    def teleopPeriodic(self):
        # teleop method, called repeatedly
        # make OI do special input things
        self.OI.handleInput()
        # move the mecanum DT w/ OI modifiers
        self.dt.handleDriving(self.OI, 0)
    
# this is NEEDED because threads are a thing
# you dont want like 5 robot code instnaces, right?
if __name__ == "__main__":
    wpilib.run(Robot)