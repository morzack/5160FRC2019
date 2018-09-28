import math

import wpilib
from wpilib.command import Subsystem

import ctre

import robotmap

from commands.intakeWithJoystick import IntakeWithJoystick


class Intake(Subsystem):
    def __init__(self, robot):
        self.robot = robot

        # get motors
        self.leftIntake = ctre.WPI_TalonSRX(robotmap.leftIntake)
        self.rightIntake = ctre.WPI_TalonSRX(robotmap.rightIntake)

        # configure motors
        self.configureMotorCurrent(self.leftIntake)
        self.configureMotorCurrent(self.rightIntake)

        # make motor group
        self.intake = wpilib.SpeedControllerGroup(self.leftIntake, self.rightIntake)
       
        super().__init__()

    def initDefaultCommand(self):
        self.setDefaultCommand(IntakeWithJoystick(self.robot))

    def useIntakeIn(self, power):
        self.intake.set(power)
    
    def useIntakeOut(self, power):
        self.intake.set(-power)

    def run(self, joystick):
        # intake motor
        if joystick.getTriggerAxis(wpilib.XboxController.Hand.kRight) > 0.1 or joystick.getY(wpilib.XboxController.Hand.kLeft) > 0.1:    # in
            self.useIntakeIn(joystick.getTriggerAxis(wpilib.XboxController.Hand.kRight) - joystick.getY(wpilib.XboxController.Hand.kLeft))
        elif joystick.getTriggerAxis(wpilib.XboxController.Hand.kLeft) > 0.1 or joystick.getY(wpilib.XboxController.Hand.kLeft) < -0.1:   # out
            self.useIntakeOut(joystick.getTriggerAxis(wpilib.XboxController.Hand.kLeft) + joystick.getY(wpilib.XboxController.Hand.kLeft))
        else:
            self.intake.set(0)

    def stop(self):
        self.intake.set(0)

    def configureMotorCurrent(self, motor):
        # configure drivetrain motors so that brownouts arent too common
        motor.configOpenLoopRamp(0.05, 100)
        motor.enableCurrentLimit(True)
        motor.configContinuousCurrentLimit(30, 100)
        motor.configPeakCurrentDuration(300, 100)
        motor.configPeakCurrentLimit(45, 100)
        motor.setNeutralMode(2) # braking is 2