import ctre
import wpilib
import OI

class Intake:
    # motor ports
    liftIntakePort = 11
    rightIntakePort = 10
    leftIntakePort = 5

    def __init__(self):
        # initialize motors
        self.liftIntakeMotor = ctre.WPI_TalonSRX(Intake.liftIntakePort)
        self.rightIntakeMotor = ctre.WPI_TalonSRX(Intake.rightIntakePort)
        self.leftIntakeMotor = ctre.WPI_TalonSRX(Intake.leftIntakePort)
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