#!/usr/bin/env python3

import wpilib
import wpilib.drive
import ctre
import logging
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

        #set up a logger
        self.logger = logging.getLogger("robot")

    def autonomousInit(self):
        # this runs before the autonomous
        # reset timer for auto
        self.timer.reset()
        self.timer.start()

        #get the alliance the robot is on
        #returns an Alliance, which is an int enum
        #0 = Red
        #1 = Blue
        #2 = Invalid
        self.alliance = wpilib.DriverStation.getInstance().getAlliance()

        #get the position the robot takes at the driver station wall
        #returns an int - 1, 2, or 3 depending on the location of the robot
        self.station = wpilib.DriverStation.getInstance().getLocation()

        #Get game specific message to determine order of plates on switches and scale
        #Make sure this runs at the END of autoInit so that the data can arrive from the FMS
        #TODO: TEST THIS - MAKE SURE THAT GAME DATA CONSISTENTLY GETS READ PROPERLY
        self.gameData = wpilib.DriverStation.getInstance().getGameSpecificMessage()

        #log if not read correctly
        #set self.gameData so the robot will know to cross the driveline insead of going to switch
        #that way, the robot will always pass the driveline even if the data isn't read correctly.
        if len(self.gameData) < 3:
            self.logger.info("Game data not read correctly!!!")
            self.gameData = "CCC"
        else:
            #sends received data
            self.logger.info("Game data read as: {}".format(self.gameData))
        

    def autonomousPeriodic(self):
        # this method is called repeatedly
        if self.timer.get() < 2.25:
            self.dt.drivetrain.driveCartesian(0, -0.4, 0)
        elif 2.25 < self.timer.get() < 4.0:
            self.dt.drivetrain.driveCartesian(0, 0, 0)  # Stop robot
        elif 4.0 < self.timer.get() < 5.0:
            self.intake.out(0.4)
        else:
            self.dt.drivetrain.driveCartesian(0, 0, 0)  # Stop robot
            self.intake.out(0.0)
    
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