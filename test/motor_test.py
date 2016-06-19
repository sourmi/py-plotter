import motor
import unittest


class TestMotor(unittest.TestCase):

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

    __gpio = motor.Gpio
    __motor= motor.Motor

    Seq1 = [0,1,0,0]
    Seq2 = [0,1,0,1]
    Seq3 = [0,0,0,1]
    Seq4 = [1,0,0,1]
    Seq5 = [1,0,0,0]
    Seq6 = [1,0,1,0]
    Seq7 = [0,0,1,0]
    Seq8 = [0,1,1,0]


    def setUp(self):
        self.__gpio = self.TestGpio()
        self.__motor = motor.FourPinStepperMotor(self.__gpio, 1,2,3,4, 0)

    def tearDown(self):
        pass

    def test_stop(self):
        self.__gpio.clear()
        self.__motor.stop()
        cmd = self.__gpio.getCommands()
        self.asserState(cmd, 1, [0,0,0,0])

    def test_forward(self):
        self.__gpio.clear()
        self.__motor.moveForward(10)

        cmd = self.__gpio.getCommands()
        self.asserState(cmd, 1, self.Seq1) # initial position
        self.asserState(cmd, 2, self.Seq2)
        self.asserState(cmd, 3, self.Seq3)
        self.asserState(cmd, 4, self.Seq4)
        self.asserState(cmd, 5, self.Seq5)
        self.asserState(cmd, 6, self.Seq6)
        self.asserState(cmd, 7, self.Seq7)
        self.asserState(cmd, 8, self.Seq8)
        self.asserState(cmd, 9, self.Seq1)
        self.asserState(cmd,10, self.Seq2)
        self.asserState(cmd,11, self.Seq3)

    def test_backward(self):
        self.__gpio.clear()
        self.__motor.moveBackward(10)

        cmd = self.__gpio.getCommands()
        self.asserState(cmd, 1, self.Seq1) # initial position
        self.asserState(cmd, 2, self.Seq8)
        self.asserState(cmd, 3, self.Seq7)
        self.asserState(cmd, 4, self.Seq6)
        self.asserState(cmd, 5, self.Seq5)
        self.asserState(cmd, 6, self.Seq4)
        self.asserState(cmd, 7, self.Seq3)
        self.asserState(cmd, 8, self.Seq2)
        self.asserState(cmd, 9, self.Seq1)
        self.asserState(cmd,10, self.Seq8)
        self.asserState(cmd,11, self.Seq7)

    def test_movement(self):
        self.__gpio.clear()
        self.__motor.moveForward(3)
        self.__motor.moveBackward(3)
        cmd = self.__gpio.getCommands()
        self.asserState(cmd, 1, self.Seq1) # initial position
        self.asserState(cmd, 2, self.Seq2)
        self.asserState(cmd, 3, self.Seq3)
        self.asserState(cmd, 4, self.Seq4)
        self.asserState(cmd, 5, self.Seq3)
        self.asserState(cmd, 6, self.Seq2)
        self.asserState(cmd, 7, self.Seq1)
        
        
    def printState(self, cmd, num):
        print self.toString(cmd, num)

    def toString(self, cmd, num):
        return "state[{0}]: {1}={2},{3}={4},{5}={6},{7}={8}".format(num
               ,cmd[(num-1)*4+0][0], cmd[(num-1)*4+0][1] \
               ,cmd[(num-1)*4+1][0], cmd[(num-1)*4+1][1] \
               ,cmd[(num-1)*4+2][0], cmd[(num-1)*4+2][1] \
               ,cmd[(num-1)*4+3][0], cmd[(num-1)*4+3][1])


    def asserState(self, cmd, num, states):
        if (
            cmd[(num-1)*4+0] == [1, states[0]]
        and cmd[(num-1)*4+1] == [2, states[1]]
        and cmd[(num-1)*4+2] == [3, states[2]]
        and cmd[(num-1)*4+3] == [4, states[3]]):
            return 1
        else:
            self.toString(cmd, num)
            self.fail("actual:"+self.toString(cmd, num)+", expected: "+str(states))

if __name__ == '__main__':
    unittest.main()
