import wpilib

class OI():
    # special buttons, handled as [joystick, button]
    reverseButton = [0, 1]  # a button
    slowButton = [0, 2]     # b button

    # input modifier constants
    slowedAmount = 0.25     # amount to slow the robot by when slowed down (cooef)

    def __init__(self):
        # set up joysticks
        self.joystick0 = wpilib.Joystick(0) # usually driver joystick
        self.joystick1 = wpilib.Joystick(1) # usually driver joystick, part 2
        self.joystick2 = wpilib.Joystick(2) # sysop stick
        self.joysticks = [self.joystick0, self.joystick1, self.joystick2]   # for easier access later
        # set up modifiers
        self.reversed = False
        self.slow = False


    def handleInput(self):
        # handle special input
        # handle reversing
        if self.joysticks[OI.reverseButton[0]].getRawButton(OI.reverseButton[1]):
            self.reversed = not self.reversed
        # handle slowing
        if self.joysticks[OI.slowButton[0]].getRawButton(OI.slowButton[1]):
            self.slow = not self.slow

    def handleNumber(self, i):
        # get the value of a number modified by the modifiers
        return (i *
                (-1 if self.reversed else 1) *
                (OI.slowedAmount if self.slow else 1))
