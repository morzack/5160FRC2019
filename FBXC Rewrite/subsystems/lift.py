import math

import wpilib
from wpilib.command import Subsystem

import ctre

import robotmap

from commands.liftWithJoystick import LiftWithJoystick


class Lift(Subsystem):
    def __init__(self, robot):
        self.robot = robot

        # get motors
        self.lift = ctre.WPI_TalonSRX(robotmap.liftIntake)

        # configure motors
        self.configureMotorCurrent(self.lift)
        
        super().__init__()

    def initDefaultCommand(self):
        self.setDefaultCommand(LiftWithJoystick(self.robot))

    def run(self, joystick):
        self.lift.set(-joystick.getY(wpilib.XboxController.Hand.kRight))

    def stop(self):
        self.lift.set(0)

    def configureMotorCurrent(self, motor):
        # configure drivetrain motors so that brownouts arent too common
        motor.configOpenLoopRamp(0.05, 100)
        motor.enableCurrentLimit(True)
        motor.configContinuousCurrentLimit(30, 100)
        motor.configPeakCurrentDuration(300, 100)
        motor.configPeakCurrentLimit(45, 100)
        motor.setNeutralMode(2) # braking is 2