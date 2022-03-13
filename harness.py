import random
import drawSvg as draw
from Connector import Connector

sheetsize = (300,250)


min_index = None
min_len = 10000
d = draw.Drawing(sheetsize[0], sheetsize[1])

k = 0
verticalLines = []
horizontalLines = []
verticalLength = 0

def drawline(pin1, pin2, render=True):
    # pin format (connector_obj, name)
    start_index = pin1[0].connectordef['pins'].index(pin1[1])
    end_index = pin2[0].connectordef['pins'].index(pin2[1])
    start_x = pin1[0].connectordef['nodes'][start_index][0]
    start_y = pin1[0].connectordef['nodes'][start_index][1]
    end_x = pin2[0].connectordef['nodes'][end_index][0]
    end_y = pin2[0].connectordef['nodes'][end_index][1]
    if render:
        p = draw.Path(stroke='black', stroke_width=1, fill='none')
    if start_y == end_y:
        #d.append(draw.Line(start_x,start_y,end_x,end_y,
        #    stroke='red', stroke_width=1, fill='none'))
        if render:
            p.M(start_x,start_y).L(end_x,end_y)
    else:
        global k, verticalLength
        k = k+1
        if render:
            p.M(start_x,start_y).L(50+10*k,start_y).L(50+10*k,end_y).L(end_x,end_y)
        #verticalLines.append((50+10*k,start_y,50+10*k,end_y))
        verticalLength += abs(start_y-end_y)
        #d.append(draw.Line(50+10*k,start_y,50+10*k,end_y,stroke_width=2,stroke='red',fill='none'))
    if render:
        d.append(p)
    if(render or r == 21846 or r >= 25000-1):
        print(verticalLength)

def run(r_, render=True):
    global d, min_index, min_len, k, verticalLength
    k=0
    verticalLength = 0
    if render:
        d.clear()
        d.append(draw.Rectangle(0,0,sheetsize[0],sheetsize[1], fill='#FFFFFF'))

    J1 = Connector(d, 10, 10, False, Connector.importConnector("DSUB9S","J1"))
    random.Random(int(r_*11)).shuffle(J1.connectordef['pins'])
    d = J1.render(render)

    J2 = Connector(d, 10, 120, False, Connector.importConnector("DSUB9S","J2"))
    random.Random(int(r_*13)).shuffle(J2.connectordef['pins'])
    d = J2.render(render)

    P1 = Connector(d, 250, 10, True, Connector.importConnector("DSUB15P","P1"))
    #P1.swap(1,7)
    random.Random(int(r_*17)).shuffle(P1.connectordef['pins'])
    d = P1.render(render)

    drawline((P1,6),(J2,5), render)
    drawline((J1,3),(P1,3), render)
    drawline((J1,5),(P1,4), render)
    drawline((J1,1),(P1,7), render)
    #drawline((J1,3),(J1,6))
    #drawline((J1,4),(J2,6))

    if verticalLength<50:
        print(r, verticalLength)

    if(verticalLength <= min_len):
        min_len = verticalLength
        min_index = r_

for r in range(25000):
    if r == 21846:
        run(r, True)
        d.saveSvg('example.svg')
        exit(0)
    else:
        run(r, False)


#run(min_index, False)

print(min_index,min_len)
d.saveSvg('example.svg')
