import motor

__motorX = motor.Motor()
__motorY = motor.Motor()

__x = 0
__y = 0

class Plotter:

    def __init__(self, motorX, motorY):
        self.__motorX = motorX
        self.__motorY = motorY
        self.__x = 0
        self.__y = 0

    def line(self, startX, startY, endX, endY):
        self.moveTo( startX, startY)
        self.lineTo(endX, endY)
        
    
    def lineTo(self, x, y):
        self.plotOn()
        self._move( x, y)
        
    
    def moveTo(self, x, y):
        self.plotOff()
        self._move( x, y)

        
    def _move(self, x, y):
        steps = max(abs(self.__x -x), abs(self.__y -y))
        if (steps==0):
            return
        dx = 1.0 *(x - self.__x) / steps
        dy = 1.0 *(y - self.__y) / steps
        #print '##', self.__x, self.__y, x, y,' ->', steps, ' dx: ', dx, ' dy: ', dy
        tx = self.__x
        ty = self.__y
        for i in range(0, int(steps)):
            tx = tx + dx
            ty = ty + dy
            rx = round(tx)
            ry = round(ty)
            #print tx, ty, '/', rx, ry, '/', self.__x, self.__y
            if rx <> self.__x:
                self.__doStep(self.__motorX, dx)
                self.__x = rx
            if ry <> self.__y:
                self.__doStep(self.__motorY, dy)
                self.__y = ry



    def __doStep(self, motor, direction):
        if (direction>0):
            motor.moveForward()
        else:
            motor.moveBackward()

    def plotOn(self):
        pass
    
    def plotOff(self):
        pass
    
    def getX(self):
        return self.__x
    
    def getY(self):
        return self.__y