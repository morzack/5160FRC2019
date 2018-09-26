from wpilib.command.commandgroup import CommandGroup
from wpilib.command.waitcommand import WaitCommand

from commands import moveDrivetrain
from commands import operateIntake

class AutoProgram(CommandGroup):
    def __init__(self):
        super().__init__('Auto Program')

        self.addSequential(moveDrivetrain.MoveDrivetrain(12, 10)) # move to switch for 10s
        self.addSequential(moveDrivetrain.TurnDrivetrain(90, 5))
        self.addSequential(WaitCommand(timeout=1))
        self.addSequential(operateIntake.IntakeOut(0.8, 3)) # shoot cube

    # NOTE: alliance station 1 is always leftmost

    def addData(self, gameData, station):
        self.gameData = gameData
        self.station = station

        if self.gameData[0] == 'L':
            self.initialL(self.station)
        elif self.gameData[0] == 'R':
            self.initialR(self.station)
        else:
            self.initialD(self.station)

    def forwards(self):
        self.addSequential(moveDrivetrain.MoveDrivetrain(120, 8))
        self.addSequential(WaitCommand(timeout=1))
        self.addSequential(moveDrivetrain.MoveDrivetrain(-10, 2))
        self.addSequential(WaitCommand(timeout=1))
    
    def eject(self):
        self.addSequential(operateIntake.IntakeOut(0.8, 3))

    def dodgeCenter(self):
        self.addSequential(moveDrivetrain.MoveDrivetrain(60, 5))
        self.addSequential(WaitCommand(timeout=1))
        self.addSequential(moveDrivetrain.TurnDrivetrain(45, 3))
        self.addSequential(moveDrivetrain.MoveDrivetrain(102, 5))

    def initialL(self, station): # left initialization, our plate on left side
        if station == 1: # pass auto line, chuck cube, nothing too fancy
            self.forwards()
            self.eject()
        if station == 2: # pass auto line to the right, DODGE CUBES
            self.dodgeCenter()
        if station == 3: # pass auto line, dont eject cube
            self.forwards()

    def initialR(self, station): # right initialization, our plate on the right side
        if station == 1: # pass auto line, dont eject cube, nothing too fancy
            self.forwards()
        if station == 2: # pass auto line to the right, DODGE CUBES
            self.dodgeCenter()
        if station == 3: # pass auto line, eject cube
            self.forwards
            self.eject()
    
    def initialD(self, station): # NANI?!? k-kansei dorifto?!?! - default initialization (CCC)
        if station == 1: # pass auto line, nothing too fancy
            self.forwards()
        if station == 2: # pass auto line to the right, DODGE CUBES
            self.dodgeCenter()
        if station == 3: # pass auto line, dont eject cube
            self.forwards()