import svg
import motor, plotter
import RPi.GPIO as GPIO

class rpiGpio(motor.Gpio):

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    def output(self, pin, value):
        #print pin, value
        GPIO.output(pin, value)

    def init(self, pin):
        GPIO.setup(pin, GPIO.OUT)

if __name__ == '__main__':
#    fileName = '../x.svg'
#    p = svg.svgParser()
#    p.parseFile(fileName)
#    for cmd in p.getCommands():
#        print cmd

    mx = motor.FourPinStepperMotor(rpiGpio(),17,18,22,23, 0.001)
    my = motor.FourPinStepperMotor(rpiGpio(), 8, 7,10, 9, 0.001)
    #x = 478 # MAX
    #mx.moveForward (x)
    #my.moveForward (x)
    #mx.moveBackward(x)
    #my.moveBackward(x)

    plotter = plotter.Plotter(mx, my)
    plotter.moveTo(0,0)
    plotter.lineTo( 50,200)
    plotter.moveTo(0,0)
    plotter.lineTo(100,200)
    plotter.moveTo(0,0)
    plotter.lineTo(150,200)
    plotter.moveTo(0,0)
    plotter.lineTo(200,200)
    plotter.moveTo(0,0)
    
    mx.stop()
    my.stop()
