
import motor

class TestGpio(motor.Gpio):

    __commands = []

    def output(self, pin, value):
        #print("output", pin,"=", value)
        self.__commands.append([pin, value])

    def init(self, pin):
        pass

    def getCommands(self):
        return self.__commands

    def clear(self):
        self.__commands = []

class Movements:
    moves = ""
    def forward(self, direction, steps):
        for i in range(0, steps):
            self.moves = self.moves + str.upper(direction) 
    def backward(self, direction, steps):
        for i in range(0, steps):
            self.moves = self.moves + str.lower(direction)
    def reset(self):
        self.moves = ""
        
        
class TestMotor(motor.Motor): 
    pos = 0
    stop = False
    name = ""
    moves = ""
    def __init__(self, name, movements):
        self.name = name
        self.moves = movements
    def moveForward(self, steps=1):
        #print self.name, "fwd", steps
        self.pos = self.pos +steps
        self.moves.forward(self.name, steps)
    def moveBackward(self, steps=1):
        #print self.name, "bwd", steps
        self.pos = self.pos - steps
        self.moves.backward(self.name, steps)
    def stop(self):
        self.stop = True
    def reset(self):
        self.pos = 0
