import xml.etree.ElementTree as ET
import re
import cmd

class SvgParser(object):

    class PathCommand(object):
        def __init__(self, cmd, coord1=None, coord2=None):
            self.cmd = cmd
            self.coord1 = coord1
            self.coord2 = coord2
            self.coCount = self.determineNeededCoords() 
        
        def isReady(self):
            if self.coCount == 0:
                return True
            if self.coCount == 1:
                if self.coord1 != None:
                    return True
            if self.coCount == 2:
                if self.coord1 != None and self.coord2 != None:
                    return True
            return False
    
        def addCoord(self, co):
            if self.coCount==0:
                # FAIL!
                return
            if self.coord1==None:
                self.coord1 = co
            elif self.coord2==None:
                self.coord2 = co
            else:
                # FAIL!
                pass
                
    
        def determineNeededCoords(self):
            if self.cmd in 'Zz':
                return 0
            elif self.cmd in 'HhVv':
                return 1
            return 2


    class PathParser(object):
        def __init__(self, d):
            p = re.compile('([a-zA-Z]{1}|-?[0-9.]+)')
            self.__iterator = p.finditer(d)
            self.commands = ()
            self.lastCmd = None
        
        def __iter__(self):
            return self
    
        def next(self):
            n = self.nextItem()
            return n
    
        def nextItem(self):
            match = self.__iterator.next()
            m = match.group()
            if m in 'LlMmZzCcHhVv':
                cmd = SvgParser.PathCommand(m)
            else:
                cmd = SvgParser.PathCommand(self.lastCmd)
                cmd.addCoord(m)
            while not cmd.isReady():
                n = self.__iterator.next().group()
                cmd.addCoord(n)
            self.lastCmd = cmd.cmd
            return cmd


    def __init__(self):
        self.__commands = []
        self.__fileName = ''
        self.__plotter = None
        self.__commands = []
        self.width = 0
        self.heigth = 0
        self.startX = None
        self.startY = None


    def getCommands(self):
        return self.__commands
    
    def clear(self):
        self.__commands = []
        self.width = 0
        self.heigth = 0
        
    def parseFile(self, fileName):
        self.__fileName=fileName
        tree = ET.parse(fileName)
        root = tree.getroot()
        vb = root.get('viewBox')
        if not vb:
            print "no viewBox defined!"
        else: 
#            self.width = vb.split()[2]
#            self.heigth = vb.split()[3]
            print "viewBox: "+ vb +"("+ str(self.width)+"/"+ str(self.heigth)+")"
        self.__parseChilds(root)
    
    def printLine(self, x1, y1, x2, y2):
        self.__append("M", x1, y1)
        self.__append("L", x2, y2)
    
    def printRect(self, x, y, width, heigth):
        x2 = str(int(x) + int(width))
        y2 = str(int(y) + int(heigth))
        self.__append("M", x , y )
        self.__append("L", x , y2)
        self.__append("L", x2, y2)
        self.__append("L", x2, y )
        self.__append("L", x , y )


    def relativeToAbsoluteCoords(self, x,y, Command):
        if Command.cmd.islower():
            if not Command.coord1:
                c1 = x
            else:
                c1 = float(Command.coord1) + float(x)
            if not Command.coord2:
                c2 = y
            else:
                c2 = float(Command.coord2) + float(y)
            Command.cmd = Command.cmd.upper()
            Command.coord1 = c1
            Command.coord2 = c2
        return Command
    
    def replaceShortcuts(self, x, y, Command):   
        if Command.cmd =='h':
            Command.coord2 = 0
            Command.cmd = 'l'
        if Command.cmd =='H':
            Command.coord2 = y
            Command.cmd = 'L'
        if Command.cmd =='V':
            Command.coord2 = Command.coord1
            Command.coord1 = x
            Command.cmd = 'L'
        if Command.cmd =='v':
            Command.coord2 = Command.coord1
            Command.coord1 = 0
            Command.cmd = 'l'

    def replaceZ(self, Command, first):
        if first:
            if Command.cmd in 'zZ':
                Command.cmd = 'L'
                Command.coord1 = first.coord1
                Command.coord2 = first.coord2

    def roundString(self, s):
        if s and '.' in s:
            s = s.rstrip('0')
            s = s.rstrip('.')
        return s
            
    def roundCoords(self, Command):
        Command.coord1 = self.roundString(str(Command.coord1))
        Command.coord2 = self.roundString(str(Command.coord2))
        return Command

    def printPath(self, d):
        return self.printPath3(d)

    def printPath3(self, d):
        p = SvgParser.PathParser(d)
        x = y = 0
        first = None
        for c in p:
            self.replaceShortcuts(x, y, c)
            self.replaceZ(c, first)
            self.relativeToAbsoluteCoords(x, y, c)
            self.roundCoords(c)
            x = c.coord1
            y = c.coord2
            if not first:
                first = c
            self.__append(c.cmd, c.coord1, c.coord2)
            
        
    def printPath1(self, d):
        parts = str(d).split()
        i =0;
        startPos = ""
        mode = 'M'
        while i < len(parts):
            if parts[i]=="M":
                mode = 'M'
                startPos = parts[i+1]
            elif parts[i]=="Z": # back to start position
                self.__append("L", startPos)
            elif parts[i]=="L" or parts[i]=="C":
                mode = 'L'
            else:
                dest = parts[i]
                self.__append(mode, dest)
            i = i+1
        
    def printPath2(self, d):
        p = re.compile('([a-zA-Z]{1}|-?[0-9.]+)')
        iterator = p.finditer(d)
        x = y =  coords= 0
        x1 = y1 = cmd = act = co1 = co2 = co = None
        ready = False
        for match in iterator:
            m = match.group()
            if m in 'LlMmZzCcHhVv':
                act = m
                cmd = act.upper()
                if cmd in 'Zz':
                    self.__append('L', x1, y1)
                elif cmd in 'HhVv':
                    coords = 1
                else:
                    coords = 2
            else:
                co = m
                if coords == 2:
                    if co1:
                        co2 = co
                        ready = True
                    else:
                        co1 = co
                else:
                    co1 = co
                    ready = True    
                if ready==True:
                    if act in 'H':
                        co2 = y 
                    if act in 'V':
                        co2 = co1
                        co1 = x
                    if act in 'h':
                        co2 = 0 
                    if act in 'v':
                        co2 = co1
                        co1 = 0
                    if act.islower():
                        co1 = float(co1)+ float(x)
                        co2 = float(co2)+ float(y)
                    x = co1
                    y = co2
                    if act in 'HVhv':
                        cmd = 'L'
                    x = self.roundString(str(x))
                    y = self.roundString(str(y))
                    if not x1:
                        x1 = x
                        y1 = y
                    self.__append(cmd, x, y)
                    ready = False
                    co1 = None
                    co2 = None
    
    def __append(self, mode, coords1, coords2=None):
        if coords2:
            self.__commands.append(mode+" "+ str(coords1)+","+str(coords2))
            self.__checkSize(coords1, coords2)
        else:
            self.__commands.append(mode+" "+ coords1)
            self.__checkSize(coords1.split(',')[0], coords1.split(',')[1])
    
    def __checkSize(self, px, py):
        x = float(px)
        y = float(py)
        if self.width<x:
            self.width = x
        if self.heigth<y:
            self.heigth = y
        if self.startX>x or self.startX==None:
            self.startX = x
        if self.startY>y or self.startY==None:
            self.startY = y
    
    def __removeNS(self, tag):
        ns = tag.find('}')
        if (ns>0) :
            tag = tag[ns+1:]
        return tag
    
    def __parseChilds(self, node):
        tag = self.__removeNS(node.tag)
        fill = node.get('fill')
        stroke = node.get('stroke')
        visible = True
        if stroke=="none" and fill=="none":
            visible = False
        if tag=="path":
            if visible:
                self.printPath(node.get('d'))
        elif tag=="rect":
            if visible:
                self.printRect(node.get('x'), node.get('x'), node.get('width'), node.get('height'))
        elif tag=="line":
            if visible:
                self.printLine(node.get('x1'), node.get('x1'), node.get('x2'), node.get('y2'))
        elif tag=="defs":
            return
        for child in node:
            self.__parseChilds(child)

    def __printChilds(self, node, prefix):
        tag = self.__removeNS(node.tag)
        print prefix, tag, node.attrib
        for child in node:
            self.__parseChilds(child, prefix+"   ")

