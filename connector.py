import drawSvg as draw

class Connector:

    def __init__(self, d, x_off, y_off, mirror, connectordef):
        self.d = d
        self.x_off = x_off
        self.y_off = y_off
        self.mirror = mirror
        self.connectordef = connectordef

    def render(self):
        pinTextHeight = 8
        pinTextMargin = 1
        pinTextColor = 'black'
        pinTextLen = 10
        # determine length of pin number boxes
        for p in self.connectordef['pins']:
            len_ = len(str(p))*pinTextHeight*.7+pinTextMargin*4
            if len_ > pinTextLen:
                pinTextLen = len_
        for i, p in enumerate(self.connectordef['pins']):
            self.d.append(draw.Rectangle(self.x_off+pinTextMargin, self.y_off+pinTextMargin+(pinTextHeight+pinTextMargin*2)*i, pinTextLen, pinTextMargin*2+pinTextHeight, stroke='black', stroke_width=1, fill='none'))
            self.d.append(draw.Text(str(p), pinTextHeight, self.x_off+pinTextMargin*2, self.y_off+(pinTextMargin*2+pinTextHeight)*i+pinTextMargin*2, fill=pinTextColor))
            if self.mirror:
                node_ = (self.x_off+pinTextMargin, self.y_off+(pinTextMargin*2+pinTextHeight)*i+pinTextMargin+(pinTextMargin*2+pinTextHeight)/2)
            else:
                node_ = (self.x_off+pinTextMargin+pinTextLen, self.y_off+(pinTextMargin*2+pinTextHeight)*i+pinTextMargin+(pinTextMargin*2+pinTextHeight)/2)
            self.connectordef['nodes'].append(node_)
            self.d.append(draw.Circle(node_[0],node_[1],1))
        # label connector
        self.d.append(draw.Text(str(self.connectordef['refdes']), 12, self.x_off, self.y_off+(pinTextMargin*2+pinTextHeight)*len(self.connectordef['pins'])+pinTextMargin*2, fill=pinTextColor))
        # TODO: Move Label and PN to
        return self.d

sheetsize = (300,250)

d = draw.Drawing(sheetsize[0], sheetsize[1])
d.append(draw.Rectangle(0,0,sheetsize[0],sheetsize[1], fill='#FFFFFF'))

connectordef = {
    'refdes': 'J1',
    'PN': 'MIL-BLAH-BLAH',
    'pins': [1, 2, 3, 4, 5, 'abc'],
    'nodes': []
}

J1 = Connector(d, 10, 10, False, connectordef)
d = J1.render()

J1 = Connector(d, 10, 100, False, connectordef)
d = J1.render()

connectordef = {
    'refdes': 'P1',
    'PN': 'MIL-BLAH-BLAH',
    'pins': [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14 ,15],
    'nodes': []
}


P1 = Connector(d, 250, 10, True, connectordef)
d = P1.render()

d.saveSvg('example.svg')