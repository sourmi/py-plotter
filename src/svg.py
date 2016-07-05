import xml.etree.ElementTree as ET

class svgParser:


    def __init__(self):
        self.__commands = []
        self.__fileName = ''
        self.__plotter = None
        self.__commands = []
        self.width = 0
        self.heigth = 0


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
            self.width = vb.split()[2]
            self.heigth = vb.split()[3]
            print "viewBox: "+ vb +"("+ self.width+"/"+ self.heigth+")"
        self.__parseChilds(root, '')
    
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
    
    def printPath(self, d):
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
            elif parts[i]=="L":
                mode = 'L'
            else:
                dest = parts[i]
                self.__append(mode, dest)
            i = i+1
    
    def __append(self, mode, coords1, coords2=None):
        if not coords2:
            self.__commands.append(mode+" "+ coords1)
            self.__checkSize(coords1.split(',')[0], coords1.split(',')[1])
        else:
            self.__commands.append(mode+" "+ coords1+","+coords2)
            self.__checkSize(coords1, coords2)
    
    def __checkSize(self, px, py):
        x = int(px)
        y = int(py)
        if self.width<x:
            self.width = x
        if self.heigth<y:
            self.heigth = y
    
    def __removeNS(self, tag):
        ns = tag.find('}')
        if (ns>0) :
            tag = tag[ns+1:]
        return tag
    
    def __parseChilds(self, node):
        tag = self.__removeNS(node.tag)
        if tag=="path":
            self.printPath(node.get('d'))
        elif tag=="rect":
            self.printRect(node.get('x'), node.get('x'), node.get('width'), node.get('height'))
        elif tag=="line":
            self.printLine(node.get('x1'), node.get('x1'), node.get('x2'), node.get('y2'))
        for child in node:
            self.__parseChilds(child)

    def __printChilds(self, node, prefix):
        tag = self.__removeNS(node.tag)
        print prefix, tag, node.attrib
        for child in node:
            self.__parseChilds(child, prefix+"   ")

