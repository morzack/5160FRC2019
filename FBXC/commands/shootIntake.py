from wpilib.command import Command

class ShootIntake(Command):
    def __init__(self, robot, time, power=0.8):
        super().__init__()
        self.requires(robot.intake)
        self.robot = robot
        self.power = power
        self.time = time

    def initialize(self):
        """Called just before this Command runs the first time."""
        self.setTimeout(self.time)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.robot.intake.useIntakeOut(self.power)

    def isFinished(self):
        """Make this return true when this Command no longer needs to run execute()"""
        return self.isTimedOut()

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.intake.stop()

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run."""
        self.end()