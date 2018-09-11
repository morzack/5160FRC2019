#!/usr/bin/env python3

import wpilib
import wpilib.drive
import ctre
from OI import *


class Robot(wpilib.IterativeRobot):
    
    # motor ports
    # DRIVETRAIN
    frontLeftPort = 1
    backLeftPort = 4
    frontRightPort = 3
    backRightPort = 2

    # compressor
    solenoidPortIn = 0
    solenoidPortOut = 1
    pcmCan = 3 # TODO

    def robotInit(self):
        # assign motors to object
        self.motorLeftFront = ctre.WPI_TalonSRX(Robot.frontLeftPort)
        self.motorLeftBack = ctre.WPI_TalonSRX(Robot.backLeftPort)
        self.motorRightFront =  ctre.WPI_TalonSRX(Robot.frontRightPort)
        self.motorRightBack = ctre.WPI_TalonSRX(Robot.backRightPort)
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
        # solenoids
        self.solenoidIn = wpilib.Solenoid(Robot.solenoidPortIn)
        self.solenoidOut = wpilib.Solenoid(Robot.solenoidPortOut)
        # valve
        self.compressor = wpilib.Compressor(Robot.pcmCan)

    def autonomousInit(self):
        # this runs before the autonomous
        # reset timer for auto
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        # this method is called repeatedly
        if self.timer.get() < 2.0:
            self.drivetrain.tankDrive(-0.8, -0.8)
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
                                        self.OI.handleNumber(-self.OI.joystick0.getY(wpilib.XboxController.Hand.kRight)))
        # set solenoids
        self.solenoidIn.set(self.OI.joystick0.getY())
        self.solenoidOut.set(self.OI.joystick0.getX())
        # set compressor
        if self.compressor.getPressureSwitchValue():
            self.compressor.start()
        else:
            self.compressor.stop()
    
# this is NEEDED because threads are a thing
# you dont want like 5 robot code instnaces, right?
if __name__ == "__main__":
    wpilib.run(Robot)