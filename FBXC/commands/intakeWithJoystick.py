from wpilib.command import Command

class IntakeWithJoystick(Command):
    def __init__(self, robot):
        super().__init__()
        self.requires(robot.intake)
        self.robot = robot

    def initialize(self):
        """Called just before this Command runs the first time."""
        pass

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.robot.intake.run(self.robot.oi.getSysop())

    def isFinished(self):
        """Make this return true when this Command no longer needs to run execute()"""
        return False

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.intake.stop()

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run."""
        self.end()