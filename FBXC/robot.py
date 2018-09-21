#!/usr/bin/env python3

import wpilib
import wpilib.drive
import ctre
from OI import *
from drivetrain import *
from intake import *

class Robot(wpilib.IterativeRobot):
    def robotInit(self):
        # setup camera
        wpilib.CameraServer.launch()
        # get drivetrain
        self.dt = Drivetrain()
        # get intake
        self.intake = Intake()
        # misc initializations
        # set up a timer to allow for cheap drive by time auto
        self.timer = wpilib.Timer()
        # initialize OI systems for the robot 
        self.OI = OI.OI()

    def autonomousInit(self):
        # this runs before the autonomous
        # reset timer for auto
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        # this method is called repeatedly
        if self.timer.get() < 3:
            self.dt.moveEncoder((14*12)-(3*12))
        elif 3 < self.timer.get() < 4.0:
            self.dt.drivetrain.driveCartesian(0, 0, 0)  # Stop robot
        elif 4.0 < self.timer.get() < 5.0:
            self.intake.outTake(0.4)
        else:
            self.dt.drivetrain.driveCartesian(0, 0, 0)  # Stop robot
            self.intake.outTake(0.0)
    
    def teleopInit(self):
        # teleop period initialization
        pass

    def teleopPeriodic(self):
        # teleop method, called repeatedly
        # make OI do special input things
        self.OI.handleInput()
        # move the mecanum DT w/ OI modifiers
        self.dt.handleDriving(self.OI, 0)
        # do stuff with intake
        self.intake.handleIntake(self.OI, 2)
    
# this is NEEDED because threads are a thing
# you dont want like 5 robot code instnaces, right?
if __name__ == "__main__":
    wpilib.run(Robot)