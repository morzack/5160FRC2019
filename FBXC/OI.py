#!/usr/bin/env python3

import wpilib
import wpilib.buttons

class OI():
    # input modifier constants
    slowedAmount = 0.8     # amount to slow the robot by when slowed down (cooef)

    def __init__(self):
        # set up joysticks
        self.joystick0 = wpilib.XboxController(0) # usually driver joystick
        self.joystick1 = wpilib.XboxController(1) # usually driver joystick, part 2
        self.joystick2 = wpilib.XboxController(2) # sysop stick
        self.joysticks = [self.joystick0, self.joystick1, self.joystick2]   # for easier access later
        # set up modifiers
        self.modifiers = {"slowed" : False, "reversed" : False}
        
    def inverseModifier(self, mod):
        self.modifiers[mod] = not self.modifiers[mod]

    def handleWithoutSpeed(self, i):
        return (i *
                (-1 if self.modifiers["reversed"] else 1))

    def handleInput(self):
        # handle special input
        if self.joystick0.getAButtonPressed(): self.inverseModifier("reversed")
        if self.joystick0.getBButtonPressed(): self.inverseModifier("slowed")

    def handleNumber(self, i):
        # get the value of a number modified by the modifiers
        return (i *
                (-1 if self.modifiers["reversed"] else 1) *
                (OI.slowedAmount if self.modifiers["slowed"] else 1))
