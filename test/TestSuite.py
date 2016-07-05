import unittest
import motor_test
import plotter_test
import svg_test

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(plotter_test.PlotterTest))
suite.addTest(unittest.makeSuite(motor_test.MotorTest))
suite.addTest(unittest.makeSuite(svg_test.SvgTest))

unittest.TextTestRunner(verbosity=2).run(suite)
