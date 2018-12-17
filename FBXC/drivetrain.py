import ctre
import wpilib
import wpilib.drive
import OI
import math

class Drivetrain:
    frontLeftPort = 2
    frontRightPort = 13
    backLeftPort = 1
    backRightPort = 14

    wheelDiameter = 6

    def __init__(self):
        # setup motors
        # assignment
        self.frontLeftMotor = ctre.WPI_TalonSRX(Drivetrain.frontLeftPort)
        self.frontRightMotor = ctre.WPI_TalonSRX(Drivetrain.frontRightPort)
        self.backLeftMotor = ctre.WPI_TalonSRX(Drivetrain.backLeftPort)
        self.backRightMotor = ctre.WPI_TalonSRX(Drivetrain.backRightPort)
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

        #handle any exceptions that arise
        try:
            # drive the robot using the oi object provided as well as the number of the controller to use
            self.drivetrain.driveCartesian(-oi.handleNumber(oi.joysticks[joystick].getX(wpilib.XboxController.Hand.kLeft)),
                                        oi.handleNumber(oi.joysticks[joystick].getY(wpilib.XboxController.Hand.kLeft)),
                                        -oi.joysticks[joystick].getX(wpilib.XboxController.Hand.kRight))
        except:
            #allow the caught exception to be raised if not connected to FMS, so that stack trace can be retreived
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

    def convertPosition(self, position):
        
        #Handle exceptions if not connected to FMS
        try:
            return position*Drivetrain.wheelDiameter*math.pi/256
        except:
            if not wpilib.DriverStation.getInstance().isFMSAttached():
                raise

    def moveEncoder(self, distance):
            self.frontLeftMotor.set(ctre.ControlMode.Position, self.convertPosition(distance))
            self.frontRightMotor.set(ctre.ControlMode.Position, self.convertPosition(distance))
            self.backLeftMotor.set(ctre.ControlMode.Position, self.convertPosition(distance))
            self.backRightMotor.set(ctre.ControlMode.Position, self.convertPosition(distance))
