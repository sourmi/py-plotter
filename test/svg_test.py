import unittest
import svg


class SvgTest(unittest.TestCase):

  
    svg = svg.svgParser()
    
    def test_printPath(self):
        self.svg.clearCommands()
        self.svg.printPath("M 1,2 L 3,4 5,6 7,8 1234567,7654321")
        self.assertCommands("M 1,2#L 3,4#L 5,6#L 7,8#L 1234567,7654321#")

    def test_printPath_WithZ(self):
        self.svg.clearCommands()
        self.svg.printPath("M 1,2 L 3,4 5,6 7,8 1234567,7654321 Z")
        self.assertCommands("M 1,2#L 3,4#L 5,6#L 7,8#L 1234567,7654321#L 1,2#")

    def test_printRect(self):
        self.svg.clearCommands()
        self.svg.printRect("0","0","10","20")
        self.assertCommands("M 0,0#L 0,20#L 10,20#L 10,0#L 0,0#")
        self.svg.clearCommands()
        self.svg.printRect("10","20","1","2")
        self.assertCommands("M 10,20#L 10,2#L 1,2#L 1,20#L 10,20#")

    def test_printLine(self):
        self.svg.clearCommands()
        self.svg.printLine("1","2","10","20")
        self.assertCommands("M 1,2#L 10,20#")
        self.svg.clearCommands()
        self.svg.printLine("10","20","1","2")
        self.assertCommands("M 10,20#L 1,2#")

    def assertCommands(self, commands):
        cmds = ""
        for cmd in self.svg.getCommands():
            cmds = cmds +cmd +"#"
        self.assertEqual(cmds, commands)
        #self.printCommands()

    def printCommands(self):
        for cmd in self.svg.getCommands():
            print cmd
