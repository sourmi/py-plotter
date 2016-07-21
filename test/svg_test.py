import unittest
import svg


class SvgTest(unittest.TestCase):

    def setUp(self):
        self.svg = svg.SvgParser()
    
    
    def test_MaxSize(self):
        self.svg.clear()
        self.assertMaxSize(0,0)
        self.svg.printPath("M 3,4 L 2,3 1,1")
        self.assertMaxSize(3,4)
        self.svg.printPath("M 1,2 L 3,4 5,6")
        self.assertMaxSize(5,6)
        self.svg.printRect("0","0","7","8")
        self.assertMaxSize(7,8)
        self.svg.printRect("7","8","3","2")
        self.assertMaxSize(10,10)
        self.svg.printLine("1","2","30","40")
        self.assertMaxSize(30,40)
        
    def assertMaxSize(self, x, y):
        self.assertEqual(x, self.svg.width)
        self.assertEqual(y, self.svg.heigth)
        

    def test_printPath(self):
        self.svg.printPath("M 1,2 L 3,4 5,6 7,8 1234567,7654321")
        self.assertCommands("M 1,2#L 3,4#L 5,6#L 7,8#L 1234567,7654321#")
        self.svg.clear()
        self.svg.printPath("M1,2L3,4-5,6-7,8 1234567,7654321z")
        self.assertCommands("M 1,2#L 3,4#L -5,6#L -7,8#L 1234567,7654321#L 1,2#")
        self.svg.clear()
        self.svg.printPath("M1.1,2.2L3.3,4.4-5.5,6.6-7.7,8.8 1234567.9,7654321.9z")
        self.assertCommands("M 1.1,2.2#L 3.3,4.4#L -5.5,6.6#L -7.7,8.8#L 1234567.9,7654321.9#L 1.1,2.2#")
        self.svg.clear()
        self.svg.printPath("M0,28l8 5 3-1")
        self.assertCommands("M 0,28#L 8,33#L 11,32#")
        
    def test_printPath_With_H_and_V(self):
        self.svg.printPath("M 1,2 H 3 V 4 L 5,6")
        self.assertCommands("M 1,2#L 3,2#L 3,4#L 5,6#")

    def test_printPath_With_lowerletter(self):
        self.svg.printPath("M 1,2 h 3 v 4 l 5,6m1,1")
        self.assertCommands("M 1,2#L 4,2#L 4,6#L 9,12#M 10,13#")

    def test_printPath_WithEndingZ(self):
        self.svg.clear()
        self.svg.printPath("M 1,2 L 3,4 5,6 7,8 1234567,7654321 Z")
        self.assertCommands("M 1,2#L 3,4#L 5,6#L 7,8#L 1234567,7654321#L 1,2#")

    def test_printRect(self):
        self.svg.clear()
        self.svg.printRect("0","0","10","20")
        self.assertCommands("M 0,0#L 0,20#L 10,20#L 10,0#L 0,0#")
        self.svg.clear()
        self.svg.printRect("1","2","10","20")
        self.assertCommands("M 1,2#L 1,22#L 11,22#L 11,2#L 1,2#")

    def test_printLine(self):
        self.svg.clear()
        self.svg.printLine("1","2","10","20")
        self.assertCommands("M 1,2#L 10,20#")
        self.svg.clear()
        self.svg.printLine("10","20","1","2")
        self.assertCommands("M 10,20#L 1,2#")

    def assertCommands(self, commands):
        cmds = ""
        for cmd in self.svg.getCommands():
            cmds = cmds +cmd +"#"
        self.assertEqual(cmds, commands)

    def printCommands(self):
        for cmd in self.svg.getCommands():
            print cmd
