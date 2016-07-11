import xml.etree.ElementTree as ET
import re

class svgParser:


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
            
    def printPath(self, d):
        p = re.compile('([a-zA-Z]{1}|-?[0-9.]+)')
        iterator = p.finditer(d)
        x1 = y1 = None
        x = 0
        y = 0
        cmd = None
        act = None
        co1 = None
        co2 = None
        co = None
        coords = 0
        first = True
        ready = False
        for match in iterator:
            m = match.group()
            if m in 'LlMmZzCcHhVv':
                act = m
                cmd = act.upper()
                if cmd in 'Zz':
                    self.__append(cmd, x1, y1)
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
                        #print '###########', cmd,act, co1,co2, x, y
                        co1 = float(co1)+ float(x)
                        co2 = float(co2)+ float(y)
                    if act in 'HVhvMm':
                        cmd = 'L'
                    x = co1
                    y = co2
                    if first:
                        cmd = 'L'
                    else:
                        cmd = 'L'
                    print '#########', cmd, x, y
                    if not x1:
                        x1 = x
                        y1 = y
                    self.__append(cmd, x, y)
                    ready = False
                    first = False
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

