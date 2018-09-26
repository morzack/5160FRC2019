import wpilib

class OI:
    def __init__(self, robot):
        self.driver = wpilib.XboxController(0)
        self.sysop = wpilib.XboxController(2)
        
        self.beastMode = True
        self.slowMode = False

        self.slowModifier = 0.6
    
    def getDriver(self):
        return self.driver

    def getSysop(self):
        return self.sysop

    def handleInput(self):
        if self.driver.getBButtonPressed(): self.beastMode = not self.beastMode
        if self.driver.getAButtonPressed(): self.slowMode = not self.slowMode

    def handleNumber(self, i):
        return (i *
                (-1 if self.beastMode else 1) *
                (self.slowModifier if self.slowMode else 1))