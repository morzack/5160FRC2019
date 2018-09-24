import ctre
import wpilib
import wpilib.drive

from wpilib.command.subsystem import Subsystem

import math

from FBXC import OI
from FBXC import robotmap

class Drivetrain(Subsystem):
    wheelDiameter = 6 # wheel diameter, in inches
    ppR = 256 # pulses of the encoder for 1 rotation

    def __init__(self):
        super().__init__('Drivetrain')
        # setup gyro
        self.gyro = wpilib.ADXRS450_Gyro()

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

        # set up encoders
        self.leftEncoder = wpilib.Encoder(aChannel=robotmap.leftEncoderChannelA, bChannel=robotmap.leftEncoderChannelB, encodingType=wpilib.encoder.Encoder.EncodingType.k4X)
        self.rightEncoder = wpilib.Encoder(aChannel=robotmap.rightEncoderChannelA, bChannel=robotmap.rightEncoderChannelB, encodingType=wpilib.encoder.Encoder.EncodingType.k4X)
        self.leftEncoder.setDistancePerPulse(Drivetrain.wheelDiameter/Drivetrain.ppR)
        self.rightEncoder.setDistancePerPulse(Drivetrain.wheelDiameter/Drivetrain.ppR)

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

    def reset(self):
        self.leftEncoder.reset()
        self.rightEncoder.reset()
        self.gyro.reset()

    def inchesToTicks(self, i):
        return i*Drivetrain.wheelDiameter*math.pi/256

    def getDistance(self):
        return (self.leftEncoder.getDistance()+self.rightEncoder.getDistance())/2

    def moveEncoder(self, distance):
        self.reset()
        tolerance = 1
        speed = 0.5
        direction = math.copysign(1, distance)
        while abs(self.getDistance()-distance) >= tolerance:
            self.drivetrain.driveCartesian(speed*distance, 0, 0)

    def turnDegrees(self, degrees):
        self.reset()
        startDeg = self.gyro.getAngle()
        # see closer direction to turn
        direction = math.copysign(1, degrees)
        tolerance = 5 # in degrees
        turnSpeed = 0.25 # ¯\_(ツ)_/¯
        while abs(self.gyro.getAngle()-degrees) >= tolerance:
            self.drivetrain.driveCartesian(0, 0, turnSpeed*direction)