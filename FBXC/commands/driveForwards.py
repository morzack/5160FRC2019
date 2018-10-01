from wpilib.command import Command

class DriveForward(Command):
    
    TOLERANCE = .1
    KP = -1.0/100.0 # TODO: This needs to be CORRECT, k?

    def __init__(self, robot, dist, maxSpeed=0.3):
        super().__init__()
        self.requires(robot.drivetrain)
        self.distance = dist
        self.driveSpeed = maxSpeed
        self.robot = robot
        self.error = 0

    def initialize(self):
        """Called just before this Command runs the first time."""
        self.robot.drivetrain.encoder.reset()
        self.setTimeout(3)
        self.robot.drivetrain.gyro.reset()

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self.error = self.distance - self.robot.drivetrain.encoder.getDistance()
        if self.driveSpeed * self.KP * self.error >= self.driveSpeed:
            self.robot.drivetrain.drivetrain.driveCartesian(0, self.driveSpeed, 0)
        else:
            self.robot.drivetrain.drivetrain.driveCartesian(0, self.driveSpeed * self.KP * self.error, 0)

    def isFinished(self):
        """Make this return true when this Command no longer needs to run execute()"""
        return abs(self.error) <= self.TOLERANCE or self.isTimedOut()

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.drivetrain.stop()

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run."""
        self.end()