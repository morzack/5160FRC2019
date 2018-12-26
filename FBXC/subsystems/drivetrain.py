import math

import wpilib
from wpilib.command import Subsystem
from wpilib.drive import mecanumdrive

import ctre

import robotmap

from commands.driveWithJoystick import DriveWithJoystick

class Drivetrain(Subsystem):
    def __init__(self, robot):
        self.robot = robot

        # get drive motors
        self.frontLeftCim = ctre.WPI_TalonSRX(robotmap.frontLeftDrive)
        self.frontRightCim = ctre.WPI_TalonSRX(robotmap.frontRightDrive)
        self.backLeftCim = ctre.WPI_TalonSRX(robotmap.backLeftDrive)
        self.backRightCim = ctre.WPI_TalonSRX(robotmap.backRightDrive)

        # configure motors
        self.configureMotorCurrent(self.frontLeftCim)
        self.configureMotorCurrent(self.frontRightCim)
        self.configureMotorCurrent(self.backLeftCim)
        self.configureMotorCurrent(self.backRightCim)

        # reverse left side motors
        self.frontLeftCim.setInverted(True)
        self.backLeftCim.setInverted(True)

        # make drivetrain
        self.drivetrain = mecanumdrive.MecanumDrive(self.frontLeftCim, self.backLeftCim, self.frontRightCim, self.backRightCim)

        # setup encoders
        self.encoderLeft = wpilib.Encoder(aChannel=robotmap.leftEncoderChannelA, bChannel=robotmap.leftEncoderChannelB, reverseDirection=False, encodingType=wpilib.Encoder.EncodingType.k4X)
        self.encoderLeft.setPIDSourceType(wpilib.Encoder.PIDSourceType.kDisplacement)
        self.encoderLeft.setDistancePerPulse((6*math.pi)/(256))
        
        self.encoderRight = wpilib.Encoder(aChannel=robotmap.rightEncoderChannelA, bChannel=robotmap.rightEncoderChannelB, reverseDirection=False, encodingType=wpilib.Encoder.EncodingType.k4X)
        self.encoderRight.setPIDSourceType(wpilib.Encoder.PIDSourceType.kDisplacement)
        self.encoderRight.setDistancePerPulse((6*math.pi)/(256))

        # setup gyro
        self.gyro = wpilib.ADXRS450_Gyro(0)

        super().__init__()

    # automatically initialize with driving with joystick
    def initDefaultCommand(self):
        self.setDefaultCommand(DriveWithJoystick(self.robot))

    # interprets input and moves the robot
    def drive(self, joystick : wpilib.XboxController):
        try:
            # drive the robot using the oi object provided as well as the number of the controller to use
            self.drivetrain.driveCartesian(self.robot.oi.handleNumber(joystick.getX(wpilib.XboxController.Hand.kLeft)),
                                        -self.robot.oi.handleNumber(joystick.getY(wpilib.XboxController.Hand.kLeft)),
                                        -joystick.getRawAxis(2) if abs(joystick.getRawAxis(2))>0.1 else 0)
        except:
            if not wpilib.DriverStation.getInstance().isFMSAttached():
                raise

    # called during E-Stop or something like that
    def stop(self):
        self.backLeftCim.set(0)
        self.backRightCim.set(0)
        self.frontLeftCim.set(0)
        self.frontRightCim.set(0)

    # reset both encoders at the same time
    def resetEncoders(self):
        self.encoderLeft.reset()
        self.encoderRight.reset()

    # get the average encoder distance
    def getAverageDistance(self):
        return (self.encoderLeft.getDistance()+self.encoderRight.getDistance())/2

    # use this to configure the motors, this should be changed as per the motor types
    def configureMotorCurrent(self, motor):
        # configure drivetrain motors so that brownouts arent too common
        motor.clearStickyFaults(0)
        motor.configOpenLoopRamp(0.2, 100)
        motor.enableCurrentLimit(True)
        motor.configContinuousCurrentLimit(55, 100)
        motor.configPeakCurrentDuration(700, 100)
        motor.configPeakCurrentLimit(65, 100)
        motor.setNeutralMode(2)