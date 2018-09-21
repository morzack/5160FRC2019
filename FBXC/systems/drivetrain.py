import ctre
import wpilib
import wpilib.drive

from wpilib.command.subsystem import Subsystem

import math

from FBXC import OI
from FBXC import robotmap

class Drivetrain(Subsystem):
    wheelDiameter = 6 # wheel diameter, in inches

    def __init__(self):
        super().__init__('Drivetrain')
        # setup motors
        # assignment
        self.frontLeftMotor = ctre.WPI_TalonSRX(robotmap.frontLeftDrive)
        self.frontRightMotor = ctre.WPI_TalonSRX(robotmap.frontRightDrive)
        self.backLeftMotor = ctre.WPI_TalonSRX(robotmap.backLeftDrive)
        self.backRightMotor = ctre.WPI_TalonSRX(robotmap.backRightDrive)

        # configure internal motor settings
        self.configureMotor(self.frontLeftMotor)
        self.configureMotor(self.frontRightMotor)
        self.configureMotor(self.backLeftMotor)
        self.configureMotor(self.backRightMotor)

        # reverse left side motors
        self.frontLeftMotor.setInverted(True)
        self.backLeftMotor.setInverted(True)

        # create drivetrain object
        self.drivetrain = wpilib.drive.MecanumDrive(self.frontLeftMotor, self.backLeftMotor, self.frontRightMotor, self.backRightMotor)

    def handleDriving(self, oi, joystick):
        try:
            # drive the robot using the oi object provided as well as the number of the controller to use
            self.drivetrain.driveCartesian(-oi.handleNumber(oi.joysticks[joystick].getX(wpilib.XboxController.Hand.kLeft)),
                                        oi.handleNumber(oi.joysticks[joystick].getY(wpilib.XboxController.Hand.kLeft)),
                                        -oi.joysticks[joystick].getX(wpilib.XboxController.Hand.kRight))
        except:
            if not wpilib.DriverStation.getInstance().isFMSAttached():
                raise

    def configureMotor(self, motor):
        # configure drivetrain motors so that brownouts arent too common
        motor.clearStickyFaults(0)
        motor.configOpenLoopRamp(0.2, 100)
        motor.enableCurrentLimit(True)
        motor.configContinuousCurrentLimit(55, 100)
        motor.configPeakCurrentDuration(700, 100)
        motor.configPeakCurrentLimit(65, 100)
        motor.setNeutralMode(2)                      # brake is 2

    def inchesToTicks(self, i):
        return i*Drivetrain.wheelDiameter*math.pi/256

    def moveEncoder(self, distance):
        self.frontLeftMotor.set(ctre.ControlMode.Position, self.inchesToTicks(distance))
        self.frontRightMotor.set(ctre.ControlMode.Position, self.inchesToTicks(distance))
        self.backLeftMotor.set(ctre.ControlMode.Position, self.inchesToTicks(distance))
        self.backRightMotor.set(ctre.ControlMode.Position, self.inchesToTicks(distance))
