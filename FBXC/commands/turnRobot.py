from wpilib.command import Command

class TurnRobot(Command):
    
    TOLERANCE = 5
    KP = -1.0/5.0 # TODO: This needs to be CORRECT, k?

    def __init__(self, robot, dist, maxSpeed=0.5, reset=True):
        super().__init__()
        self.requires(robot.drivetrain)
        self.distance = dist
        self.driveSpeed = maxSpeed
        self.reset = reset
        self.robot = robot
        self.error = 0

    def initialize(self):
        """Called just before this Command runs the first time."""
        if self.reset:
            self.robot.drivetrain.gyro.reset()
        self.setTimeout(4)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.error = self.distance - self.robot.drivetrain.gyro.getAngle()
        if self.driveSpeed * self.KP * self.error >= self.driveSpeed:
            self.robot.drivetrain.drivetrain.driveCartesian(0, 0, self.driveSpeed)
        else:
            self.robot.drivetrain.drivetrain.driveCartesian(0, 0, self.driveSpeed * self.KP * self.error)

    def isFinished(self):
        """Make this return true when this Command no longer needs to run execute()"""
        return abs(self.error) <= self.TOLERANCE or self.isTimedOut()

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.drivetrain.stop()

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run."""
        self.end()