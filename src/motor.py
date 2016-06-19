import time


class Motor(object):

    def moveForward(self, steps=1):
        pass

    def moveBackward(self, steps=1):
        pass

    def stop(self):
        pass


class Gpio:

    def output(self, pin, value):
        pass
        # GPIO.output(pin, value)

    def init(self, pin):
        pass
        # GPIO.setup(pin, GPIO.OUT)


class FourPinStepperMotor:

    __MIN_MOVE_DELAY = 0.001
    _delay = __MIN_MOVE_DELAY

    __StepCount = 8;
    __Seq = range(0, __StepCount)
    __Seq[0] = [0,1,0,0]
    __Seq[1] = [0,1,0,1]
    __Seq[2] = [0,0,0,1]
    __Seq[3] = [1,0,0,1]
    __Seq[4] = [1,0,0,0]
    __Seq[5] = [1,0,1,0]
    __Seq[6] = [0,0,1,0]
    __Seq[7] = [0,1,1,0]

    __counter = 0;
    __pins = range(0,4)
    __gpio = Gpio()


    def stop(self):
        self.__setPinStates([0,0,0,0])

    def moveForward(self, steps=1):
        self.__move(1, steps)

    def moveBackward(self, steps=1):
        self.__move(-1, steps)


    def __init__(self, gpio, pin1, pin2, pin3, pin4, delay):
        self.__pins[0] = pin1
        self.__pins[1] = pin2
        self.__pins[2] = pin3
        self.__pins[3] = pin4
        self.__gpio = gpio
        if delay >= self.__MIN_MOVE_DELAY:
            self._delay=delay
        else:
            self._delay=self.__MIN_MOVE_DELAY

        # initialize pins
        for i in range(len(self.__pins)):
            self.__initPin(self.__pins[i])

        # set the motor to start position
        self.moveBackward(self.__StepCount)
        self.stop()
        self.__counter=False

    
    def __setPinState(self, pin, value):
        self.__gpio.output(pin, value)

    def __initPin(self, pin):
        self.__gpio.init(pin)

    def __setPinStates(self, values):
        for i in range(len(self.__pins)):
                self.__setPinState(self.__pins[i], values[i])


    def __move(self, direction, steps=1):
        #set initial position
        if not self.__counter:
            self.__counter = 0
            self.__setPinStates(self.__Seq[0])
            time.sleep(self._delay)
        for i in range(0, steps):
            self.__counter=self.__counter +direction
            self.__setPinStates(self.__Seq[self.__counter%self.__StepCount])
            time.sleep(self._delay)
