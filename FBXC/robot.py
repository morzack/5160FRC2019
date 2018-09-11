#!/usr/bin/env python3

import wpilib
import wpilib.drive
import ctre
from OI import *


class Robot(wpilib.IterativeRobot):
    
    # motor ports
    # DRIVETRAIN
    frontLeftPort = 2
    backLeftPort = 1
    frontRightPort = 13
    backRightPort = 14
    # INTAKE
    intakeLiftPort = 11
    intakeRightPort = 10
    intakeLeftPort = 5

    def robotInit(self):
        # initialize drivetrain
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
        self.drivetrain = wpilib.drive.MecanumDrive(self.motorLeftFront, self.motorLeftBack, self.motorRightFront, self.motorRightBack)
        
        # initalize intake
        # assign motors
        self.motorIntakeLift = ctre.WPI_TalonSRX(Robot.intakeLiftPort)
        self.motorIntakeRight = ctre.WPI_TalonSRX(Robot.intakeRightPort)
        self.motorIntakeLeft = ctre.WPI_TalonSRX(Robot.intakeLeftPort)
        # invert motors
        self.motorIntakeLeft.setInverted(True)
        # make motor group
        self.intakeMotors = wpilib.SpeedControllerGroup(self.motorIntakeLeft, self.motorIntakeRight)

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
            self.drivetrain.driveCartesian(0.8, 0, 0)
        else:
            self.drivetrain.driveCartesian(0, 0, 0)  # Stop robot
    
    def teleopInit(self):
        # teleop period initialization
        pass

    def teleopPeriodic(self):
        # teleop method, called repeatedly
        # make OI do special input things
        self.OI.handleInput()
        # move the mecanum DT w/ OI modifiers
        self.drivetrain.driveCartesian(self.OI.handleNumber(self.OI.joystick0.getX(wpilib.XboxController.Hand.kLeft)),
                                        self.OI.handleNumber(self.OI.joystick0.getY(wpilib.XboxController.Hand.kLeft)),
                                        self.OI.handleNumber(-1 * self.OI.joystick0.getX(wpilib.XboxController.Hand.kRight)))

        #out

        if self.OI.joystick2.getTriggerAxis(wpilib.XboxController.Hand.kRight) > 0.1:
            self.motorIntakeLeft.set(self.OI.joystick2.getTriggerAxis(wpilib.XboxController.Hand.kRight))
            self.motorIntakeRight.set(-1 * self.OI.joystick2.getTriggerAxis(wpilib.XboxController.Hand.kRight))

        #in
        if self.OI.joystick2.getTriggerAxis(wpilib.XboxController.Hand.kLeft) > 0.1:
            self.motorIntakeLeft.set(-1 * self.OI.joystick2.getTriggerAxis(wpilib.XboxController.Hand.kLeft))
            self.motorIntakeRight.set(self.OI.joystick2.getTriggerAxis(wpilib.XboxController.Hand.kLeft))

        if self.OI.joystick2.getTriggerAxis(wpilib.XboxController.Hand.kLeft) < 0.1 and self.OI.joystick2.getTriggerAxis(wpilib.XboxController.Hand.kRight) < 0.1:
            self.motorIntakeLeft.set(0)
            self.motorIntakeRight.set(0)

        #lift
        self.motorIntakeLift.set(self.OI.joystick2.getY(wpilib.XboxController.Hand.kRight))
    
# this is NEEDED because threads are a thing
# you dont want like 5 robot code instnaces, right?
if __name__ == "__main__":
    wpilib.run(Robot)