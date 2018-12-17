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
    # TODO Get Real Numbers
    leftSolenoidIn = 4
    leftSolenoidOut = 5
    rightSolenoidIn = 2
    rightSolenoidOut = 3

    pcmCan = 0


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
        self.leftSolenoid = wpilib.DoubleSolenoid(Robot.leftSolenoidIn, Robot.leftSolenoidOut)
        self.rightSolenoid = wpilib.DoubleSolenoid(Robot.rightSolenoidIn, Robot.rightSolenoidOut)


    def autonomousInit(self):
        # this runs before the autonomous
        # reset timer for auto
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        # this method is called repeatedly
        # if self.timer.get() < 2.0:
        #     self.drivetrain.tankDrive(-0.8, -0.8)
        # else:
        #     self.drivetrain.tankDrive(0, 0)  # Stop robot
        pass

    
    def teleopInit(self):
        # teleop period initialization
        pass


    def teleopPeriodic(self):
        # teleop method, called repeatedly
        # make OI do special input things
        self.OI.handleInput()
        # move the mecanum DT w/ OI modifiers
        self.drivetrain.tankDrive(self.OI.handleNumber(-self.OI.joystick0.getY(wpilib.XboxController.Hand.kRight)),
                                        self.OI.handleNumber(self.OI.joystick0.getY(wpilib.XboxController.Hand.kLeft)))
        # set solenoids
        if self.OI.joystick0.getTriggerAxis(wpilib.Joystick.Hand.kRight) >= 0.1:
            self.leftSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)
            self.rightSolenoid.set(wpilib.DoubleSolenoid.Value.kForward)
        elif self.OI.joystick0.getTriggerAxis(wpilib.Joystick.Hand.kLeft) >= 0.1:
            self.leftSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
            self.rightSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
        else:
            self.leftSolenoid.set(wpilib.DoubleSolenoid.Value.kOff)
            self.rightSolenoid.set(wpilib.DoubleSolenoid.Value.kOff)
            
        
    
# this is NEEDED because threads are a thing
# you dont want like 5 robot code instnaces, right?
if __name__ == "__main__":
    wpilib.run(Robot)