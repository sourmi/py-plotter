import svg

if __name__ == '__main__':
    p = svg.svgParser()
    p.parseFile('/home/x/git/py-plotter/x.svg')
    cmds = p.getCommands()
    for cmd in cmds:
        print cmd
    