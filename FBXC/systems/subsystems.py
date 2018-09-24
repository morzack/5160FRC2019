from systems import drivetrain
from systems import intake

dt = None
inT = None

def init():
    global dt
    global inT

    dt = drivetrain.Drivetrain()
    inT = intake.Intake()