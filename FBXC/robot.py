#!/usr/bin/env python3

import wpilib
import wpilib.drive
import ctre

from commandbased import CommandBasedRobot
from commands import autonomousProgram

import logging

import OI
import robotmap
from systems import subsystems

class Robot(CommandBasedRobot):
    def robotInit(self):
        # setup camera server
        wpilib.CameraServer.launch()
        
        # initialize subsystems
        subsystems.init()
        
        # misc initializations
        # set up a timer to allow for cheap drive by time auto
        self.timer = wpilib.Timer()
        
        # initialize OI systems for the robot 
        self.OI = OI.OI()

        #set up a logger
        self.logger = logging.getLogger("robot")

        # auto program
        self.autoProgram = autonomousProgram.AutoProgram()

    def autonomousInit(self):
        # this runs before the autonomous
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
        
        # run autonomous
        self.autoProgram.start()

    def teleopInit(self):
        # teleop period initialization
        pass

    def teleopPeriodic(self):
        # teleop method, called repeatedly
        # make OI do special input things
        self.OI.handleInput()

        # move the mecanum DT w/ OI modifiers
        subsystems.dt.handleDriving(self.OI, 0)
        
        # do stuff with intake
        subsystems.inT.handleIntake(self.OI, 2)
    
# this is NEEDED because threads are a thing
# you dont want like 5 robot code instnaces, right?
if __name__ == "__main__":
    wpilib.run(Robot)