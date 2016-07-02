import xml.etree.ElementTree as ET

class svgParser:

    __fileName = ''
    __plotter = None
    __commands = []

    def __init__(self):
        __commands = []

    def getCommands(self):
        return self.__commands
    
    def clearCommands(self):
        self.__commands = []
        
    def parseFile(self, fileName):
        self.__fileName=fileName
        tree = ET.parse(fileName)
        root = tree.getroot()
        print "root: ", self.__removeNS(root.tag),"viewBox: ", root.get('viewBox')
        self.__printChilds(root, '')
    
    def printLine(self, x1, y1, x2, y2):
        self.__append("M", x1, y1)
        self.__append("L", x2, y2)
    
    def printRect(self, x, y, width, heigth):
        self.__append("M", x, y)
        self.__append("L", x, heigth)
        self.__append("L", width, heigth)
        self.__append("L", width, y)
        self.__append("L", x, y)
    
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
        else:
            self.__commands.append(mode+" "+ coords1+","+coords2)
    
    
    def __removeNS(self, tag):
        ns = tag.find('}')
        if (ns>0) :
            tag = tag[ns+1:]
        return tag
    
    def __printChilds(self, node, prefix):
        tag = self.__removeNS(node.tag)
        if tag=="path":
            self.printPath(node.get('d'))
        elif tag=="rect":
            self.printRect(node.get('x'), node.get('x'), node.get('width'), node.get('height'))
        elif tag=="line":
            self.printLine(node.get('x1'), node.get('x1'), node.get('x2'), node.get('y2'))
        print prefix, tag, node.attrib
        for child in node:
            self.__printChilds(child, prefix+"   ")

