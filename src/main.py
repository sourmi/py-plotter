import svg

if __name__ == '__main__':
    fileName = '../x.svg'
    p = svg.svgParser()
    p.parseFile(fileName)
    for cmd in p.getCommands():
        print cmd
    