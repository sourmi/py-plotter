import motor
import unittest
import plotter

class TestPlotter(unittest.TestCase):

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
            
    moves = Movements()
    motorX = TestMotor("x", moves)
    motorY = TestMotor("y", moves)
    plotter = plotter.Plotter(motorX, motorY)


    def test_threePartsSameResultAsAllInOne(self):
        self.reset()
        self.plotter.lineTo(60,30)
        moves_aio = self.moves.moves
        self.reset()
        self.plotter.lineTo(20,10)
        self.plotter.lineTo(40,20)
        self.plotter.lineTo(60,30)
        moves_parts = self.moves.moves
        self.assertEqual(moves_aio, moves_parts)

    def test_twoPartsSameResultAsAllInOne(self):
        self.reset()
        self.plotter.lineTo(4,4)
        self.assertEqual(self.moves.moves, "XYXYXYXY")
        self.reset()
        self.plotter.lineTo(2,2)
        self.plotter.lineTo(4,4)
        self.assertEqual(self.moves.moves, "XYXYXYXY")

    
    def test_square(self):
        self.reset()
        self.plotter.lineTo(4,0)
        self.plotter.lineTo(4,4)
        self.plotter.lineTo(0,4)
        self.plotter.lineTo(0,0)
        self.assertPos(0,0)
        self.assertEqual(self.moves.moves, "XXXXYYYYxxxxyyyy")
        
        

    def test_lineTo(self):
        self.assertMove(-1,-1, "xy")
        self.assertMove( 1,-1, "Xy")
        self.assertMove(-1, 1, "xY")
        self.assertMove( 1, 1, "XY")
        self.assertMove(-4,-2, "xyxxyx")
        self.assertMove(-4, 2, "xYxxYx")
        self.assertMove( 4,-2, "XyXXyX")
        self.assertMove( 4, 2, "XYXXYX")
        self.assertMove(-4, 4, "xYxYxYxY")
        self.assertMove( 4,-4, "XyXyXyXy")
        self.assertMove( 4, 4, "XYXYXYXY")
        self.assertMove(-4,-4, "xyxyxyxy")
        self.assertMove( 4, 0, "XXXX")
        self.assertMove(-4, 0, "xxxx")
        self.assertMove( 0, 4, "YYYY")
        self.assertMove( 0,-4, "yyyy")
        self.assertMove( 0, 0, "")

    def assertMove(self, x,y, steps):
        self.reset()
        self.plotter.lineTo(x,y)
        self.assertPos(x,y)
        self.assertEqual(self.moves.moves, steps)


    def assertPos(self, x, y):
        self.assertEqual(self.plotter.getX(), x)
        self.assertEqual(self.plotter.getY(), y)
        self.assertEqual(self.motorX.pos, x)
        self.assertEqual(self.motorY.pos, y)

    def reset(self):
        self.plotter.lineTo(0,0)
        self.moves.reset()
        self.motorX.reset()
        self.motorY.reset()
