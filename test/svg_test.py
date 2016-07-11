import unittest
import svg


class SvgTest(unittest.TestCase):

    def setUp(self):
        self.svg = svg.svgParser()
    
    
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
        

    def test_printPath2(self):
        self.svg.clear()
        self.svg.printPath2("m403.43 677.18-17.775-21.901-25.393-13.014-12.696 0.63482-12.062 4.4438-4.1264 6.983h-10.475l8.2527 5.7134")
        #self.svg.printPath2("M 1,2 L 3,4 -5,6 -7,8 1234567,7654321")
        #self.svg.printPath2("M1,2L3,4-5,6-7,8 1234567,7654321")
        self.assertCommands("M 1,2#L 3,4#L -5,6#L -7,8#L 1234567,7654321#")

    
    def test_printPath(self):
        self.svg.clear()
        self.svg.printPath("M 1,2 L 3,4 5,6 7,8 1234567,7654321")
        self.assertCommands("M 1,2#L 3,4#L 5,6#L 7,8#L 1234567,7654321#")

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
