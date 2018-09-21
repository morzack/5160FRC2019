import ctre
import wpilib

from wpilib.command.subsystem import Subsystem

from FBXC import OI
from FBXC import robotmap

class Intake(Subsystem):
    def __init__(self):
        super().__init__('Intake')
        # initialize motors
        self.liftIntakeMotor = ctre.WPI_TalonSRX(robotmap.liftIntake)
        self.rightIntakeMotor = ctre.WPI_TalonSRX(robotmap.rightIntake)
        self.leftIntakeMotor = ctre.WPI_TalonSRX(robotmap.leftIntake)
 
        # configure motors
        self.configureMotor(self.liftIntakeMotor)
        self.configureMotor(self.rightIntakeMotor)
        self.configureMotor(self.leftIntakeMotor)
 
        # invert motors
        # self.leftIntakeMotor.setInverted(True)
 
        # make motor group
        self.intakeMotors = wpilib.SpeedControllerGroup(self.leftIntakeMotor, self.rightIntakeMotor)

    def handleIntake(self, oi, joystick):
        # intake motor
        if oi.joysticks[joystick].getTriggerAxis(wpilib.XboxController.Hand.kRight) > 0.1:                        # in
            self.inTake(oi.joysticks[joystick].getTriggerAxis(wpilib.XboxController.Hand.kLeft))
        elif oi.joysticks[joystick].getTriggerAxis(wpilib.XboxController.Hand.kLeft) > 0.1:                       # out
            self.outTake(oi.joysticks[joystick].getTriggerAxis(wpilib.XboxController.Hand.kLeft))
        else:
            self.intakeMotors.set(0)
 
        #lift
        self.liftIntakeMotor.set(-oi.joysticks[joystick].getY(wpilib.XboxController.Hand.kRight))

    def outTake(self, power):
        self.intakeMotors.set(-power)
        # self.leftIntakeMotor.set(power)
        # self.rightIntakeMotor.set(-power)

    def inTake(self, power):
        self.intakeMotors.set(power)

    def configureMotor(self, motor):
        # configure drivetrain motors so that brownouts arent too common
        motor.configOpenLoopRamp(0.05, 100)
        motor.enableCurrentLimit(True)
        motor.configContinuousCurrentLimit(30, 100)
        motor.configPeakCurrentDuration(300, 100)
        motor.configPeakCurrentLimit(45, 100)
        motor.setNeutralMode(2) # braking is 2