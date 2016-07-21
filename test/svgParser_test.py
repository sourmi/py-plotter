import unittest
import svg


class SvgParserTest(unittest.TestCase):

    def setUp(self):
        pass


    def test_parser_parseCoordsOnly(self):
        p = svg.PathParser("M 1,2 3,4 5,6 v 7 h 8 l-1-2-3-4m-5-6-7-8Z")
        self.assetCommand(p.next(), "M", "1", "2")
        self.assetCommand(p.next(), "M", "3", "4")
        self.assetCommand(p.next(), "M", "5", "6")
        self.assetCommand(p.next(), "v", "7")
        self.assetCommand(p.next(), "h", "8")
        self.assetCommand(p.next(), "l", "-1", "-2")
        self.assetCommand(p.next(), "l", "-3", "-4")
        self.assetCommand(p.next(), "m", "-5", "-6")
        self.assetCommand(p.next(), "m", "-7", "-8")
        self.assetCommand(p.next(), "Z")

    def test_parser_parseUpper(self):
        p = svg.PathParser("M 1,2 L 3,4 H 5 V 6 Z")
        self.assetCommand(p.next(), "M", "1", "2")
        self.assetCommand(p.next(), "L", "3", "4")
        self.assetCommand(p.next(), "H", "5")
        self.assetCommand(p.next(), "V", "6")
        self.assetCommand(p.next(), "Z")

    def test_parser_parseLower(self):
        p = svg.PathParser("m 1,2 l 3,4 h 5 v 6 z")
        self.assetCommand(p.next(), "m", "1", "2")
        self.assetCommand(p.next(), "l", "3", "4")
        self.assetCommand(p.next(), "h", "5")
        self.assetCommand(p.next(), "v", "6")
        self.assetCommand(p.next(), "z")


    def test_command_addCoord(self):
        cmd = self.createCmd("m", "1", "2", "3")
        self.assetCoords(cmd, "1", "2")


    def test_comman_determineNeededCoords(self):
        self.assertEqual(svg.PathCommand('m').coCount, 2)
        self.assertEqual(svg.PathCommand('M').coCount, 2)
        self.assertEqual(svg.PathCommand('L').coCount, 2)
        self.assertEqual(svg.PathCommand('l').coCount, 2)
        self.assertEqual(svg.PathCommand('h').coCount, 1)
        self.assertEqual(svg.PathCommand('H').coCount, 1)
        self.assertEqual(svg.PathCommand('v').coCount, 1)
        self.assertEqual(svg.PathCommand('V').coCount, 1)
        self.assertEqual(svg.PathCommand('z').coCount, 0)
        self.assertEqual(svg.PathCommand('Z').coCount, 0)


    def createCmd(self, PathCommand, co1=None, co2=None, co3=None):
        cmd = svg.PathCommand(PathCommand)
        cmd.addCoord(co1)
        cmd.addCoord(co2)
        cmd.addCoord(co3)
        return cmd

    def assetCommand(self,PathCommand, cmd, co1=None, co2=None):
        self.assertEqual(PathCommand.cmd, cmd)
        self.assertEqual(PathCommand.coord1, co1)
        self.assertEqual(PathCommand.coord2, co2)

    def assetCoords(self, cmd, co1, co2):
        self.assertEqual(cmd.coord1, co1)
        self.assertEqual(cmd.coord2, co2)

    def assertCommands(self, commands):
        cmds = ""
        for cmd in self.svg.getCommands():
            cmds = cmds +cmd +"#"
        self.assertEqual(cmds, commands)

    def printCommands(self):
        for cmd in self.svg.getCommands():
            print cmd
