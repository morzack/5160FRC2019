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
        self.leftIntakeMotor.setInverted(True)
        # make motor group
        self.intakeMotors = wpilib.SpeedControllerGroup(self.leftIntakeMotor, self.rightIntakeMotor)

    def handleIntake(self, oi, joystick):
        # intake motor
        if oi.joysticks[joystick].getTriggerAxis(wpilib.XboxController.Hand.kRight) > 0.1:                        # out
            self.leftIntakeMotor.set(oi.joysticks[joystick].getTriggerAxis(wpilib.XboxController.Hand.kRight))
            self.rightIntakeMotor.set(oi.joysticks[joystick].getTriggerAxis(wpilib.XboxController.Hand.kRight))
        elif oi.joysticks[joystick].getTriggerAxis(wpilib.XboxController.Hand.kLeft) > 0.1:                       # in
            self.leftIntakeMotor.set(oi.joysticks[joystick].getTriggerAxis(wpilib.XboxController.Hand.kLeft))
            self.rightIntakeMotor.set(oi.joysticks[joystick].getTriggerAxis(wpilib.XboxController.Hand.kLeft))
        else:
            self.leftIntakeMotor.set(0)
            self.rightIntakeMotor.set(0)
        #lift
        self.liftIntakeMotor.set(oi.joysticks[joystick].getY(wpilib.XboxController.Hand.kRight))

    def configureMotor(self, motor):
        # configure drivetrain motors so that brownouts arent too common
        motor.clearStickyFaults(0)
        motor.configOpenLoopRamp(0.2, 100)
        motor.enableCurrentLimit(True)
        motor.configContinuousCurrentLimit(55, 100)
        motor.configPeakCurrentDuration(700, 100)
        motor.configPeakCurrentLimit(65, 100)
        motor.setNeutralMode(2)                      # brake is 2