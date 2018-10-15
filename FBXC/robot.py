#!/usr/bin/env python3

import wpilib
from wpilib.command import Scheduler

from OI import OI

import logging

from subsystems import drivetrain, intake, lift

from commands import passAutoLineShoot, centerDodge, passAutoLine, spinBot

from robotpy_ext.autonomous import AutonomousModeSelector

class Robot(wpilib.IterativeRobot):
    def robotInit(self):
        self.drivetrain = drivetrain.Drivetrain(self)
        self.intake = intake.Intake(self)
        self.lift = lift.Lift(self)

        self.oi = OI(self)

        self.logger = logging.getLogger("robot")

        self.autonomousCommand = None

        wpilib.CameraServer.launch('vision.py:main')

        self.chooser = wpilib.SendableChooser()
        self.chooser.addObject("Left", 1)
        self.chooser.addDefault("Center", 2)
        self.chooser.addObject("Right", 3)

        wpilib.SmartDashboard.putData("Auto Chooser", self.chooser)

    def chooseAuto(self, station, field):
        closest = field[0]
        if station == 2:
            if closest=="L":
                self.autonomousCommand = spinBot.SpinBot(self)
            elif closest=="R":
                self.autonomousCommand = centerDodge.CenterDodgeRight(self)
            else:
                self.autonomousCommand = centerDodge.CenterDodge(self)
        elif closest=="L":
            if station == 1:
                self.autonomousCommand = passAutoLineShoot.PassAutoLineShoot(self)
            elif station == 3:
                self.autonomousCommand = passAutoLine.PassAutoLine(self)
        elif closest=="R":
            if station == 1:
                self.autonomousCommand = passAutoLine.PassAutoLine(self)
            elif station == 3:
                self.autonomousCommand = passAutoLineShoot.PassAutoLineShoot(self)
        else:
            self.autonomousCommand = centerDodge.CenterDodge(self)

    def autonomousInit(self):
        # get field data for auto
        alliance = wpilib.DriverStation.getInstance().getAlliance()

        # get the position the robot takes at the driver station wall
        # returns an int - 1, 2, or 3 depending on the location of the robot
        station = self.chooser.getSelected()
        if not (station in [1, 2, 3]):
           station = wpilib.DriverStation.getInstance().getLocation()
        
        # Get game specific message to determine order of plates on switches and scale
        # Make sure this runs at the END of autoInit so that the data can arrive from the FMS
        gameData = wpilib.DriverStation.getInstance().getGameSpecificMessage()

        # log if not read correctly
        # set self.gameData so the robot will know to cross the driveline insead of going to switch
        # that way, the robot will always pass the driveline even if the data isn't read correctly.
        if len(gameData) < 3:
            self.logger.info("Game data not read correctly!!!")
            gameData = "CCC"
        else:
            # sends received data
            self.logger.info("Game data read as: {}".format(gameData))

        self.chooseAuto(station, gameData)

        # self.chooseAuto(station, gameData)
        self.autonomousCommand.start()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous"""
        Scheduler.getInstance().run()
        self.log()

    def teleopInit(self):
        """This function is called at the beginning of operator control."""
        #This makes sure that the autonomous stops running when
        #teleop starts running. If you want the autonomous to
        #continue until interrupted by another command, remove
        #this line or comment it out.
        if self.autonomousCommand is not None:
            self.autonomousCommand.cancel()
        self.drivetrain.encoder.reset()

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        Scheduler.getInstance().run()
        self.log()

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        # wpilib.LiveWindow.run()
        pass

    def disabledInit(self):
        pass

    def disabledPeriodic(self):
        """This function is called periodically while disabled."""
        self.log()

    def log(self):
        # print("bl SRX %s" % self.drivetrain.backLeftCim.getOutputCurrent())
        # print("br SRX %s"  % self.drivetrain.backLeftCim.getOutputCurrent())
        # print("fl SRX %s"  % self.drivetrain.backLeftCim.getOutputCurrent())
        # print("fr SRX %s"  % self.drivetrain.backLeftCim.getOutputCurrent())
        pass

if __name__ == "__main__":
    wpilib.run(Robot)