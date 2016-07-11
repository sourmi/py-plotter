import Image
import plotter, motor, svg

width = 600

img = Image.new( 'RGB', (width,width), "black") # create a new black image
pixels = img.load() # create the pixel map

class GuiMotor(object):
    def __init__(self):
        self.pos =0
    def moveForward(self, steps=1):
        self.pos = self.pos +steps
        putPixel()
    def moveBackward(self, steps=1):
        self.pos = self.pos - steps
        putPixel()
    def stop(self):
        pass

class GuiTool(object):
    def __init__(self):
        self.mode = 0
    def on(self):
        self.mode = 1
    def off(self):
        self.mode = 0

def putPixel():
    if (tool.mode==1):
        pixels[xm.pos,ym.pos] = (200,200,200)


xm = GuiMotor()
ym = GuiMotor()
tool = GuiTool()
plotter = plotter.Plotter(xm,ym, tool)
#fileName = '../x.svg'
fileName = '../horse-2.svg'
#fileName = '../tux-caveman_02.svg'
p = svg.svgParser()
p.parseFile(fileName)
sx = int(p.startX)
sy = int(p.startY)
wx = int(p.width ) - sx
wy = int(p.heigth) - sy
fx = float(float(width-20) / float(wx )) 
fy = float(float(width-20) / float(wy )) 

print p.startX, p.width , sx, wx, fx
print p.startY, p.heigth, sy, wy, fy

factor = min(fx, fy)
print factor
for cmd in p.getCommands():
    parts = cmd.split()
    mode = parts[0]
    coords = parts[1].split(',')
    x = int((float(coords[0])-sx)*factor) +1
    y = int((float(coords[1])-sy)*factor) +1
    #print coords[0], sx, x, tool.mode
    if mode=='M':
        plotter.moveTo(x, y)
    else:
        plotter.lineTo(x, y)


#for i in range(img.size[0]):    # for every pixel:
#    for j in range(img.size[1]):
#        pixels[i,j] = (i, 100, 100) # set the colour accordingly

img.show()