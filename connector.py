import drawSvg as draw
import yaml

class Connector:

    connectorList = {}

    def __init__(self, d, x_off, y_off, mirror, connectordef):
        self.d = d
        self.x_off = x_off
        self.y_off = y_off
        self.mirror = mirror
        self.connectordef = connectordef

    def render(self, render=True):
        pinTextHeight = 8
        pinTextMargin = 1
        pinTextColor = "black"
        pinTextLen = 10
        self.connectordef['nodes'] = []
        # determine length of pin number boxes
        for p in self.connectordef['pins']:
            len_ = len(str(p))*pinTextHeight*.7+pinTextMargin*4
            if len_ > pinTextLen:
                pinTextLen = len_
        for i, p in enumerate(self.connectordef['pins']):
            if self.mirror:
                node_ = (self.x_off+pinTextMargin, int(self.y_off+(pinTextMargin*2+pinTextHeight)*i+pinTextMargin+(pinTextMargin*2+pinTextHeight)/2))
            else:
                node_ = (self.x_off+pinTextMargin+pinTextLen, int(self.y_off+(pinTextMargin*2+pinTextHeight)*i+pinTextMargin+(pinTextMargin*2+pinTextHeight)/2))
            self.connectordef['nodes'].append(node_)
            if render:
                self.d.append(draw.Rectangle(self.x_off+pinTextMargin, self.y_off+pinTextMargin+(pinTextHeight+pinTextMargin*2)*i, pinTextLen, pinTextMargin*2+pinTextHeight, stroke='black', stroke_width=1, fill='none'))
                self.d.append(draw.Text(str(p), pinTextHeight, self.x_off+pinTextMargin*2, self.y_off+(pinTextMargin*2+pinTextHeight)*i+pinTextMargin*2, fill=pinTextColor))
                self.d.append(draw.Circle(node_[0],node_[1],1))
        # label connector
        if render:
            self.d.append(draw.Text(str(self.connectordef['refdes']), 12, self.x_off, self.y_off+(pinTextMargin*2+pinTextHeight)*len(self.connectordef['pins'])+pinTextMargin*2, fill=pinTextColor))
        # TODO: Move Label and PN to
        return self.d

    def swap(self, pin1, pin2):
        pin1_index = self.connectordef['pins'].index(pin1)
        pin2_index = self.connectordef['pins'].index(pin2)
        temp = self.connectordef['pins'][pin1_index]
        self.connectordef['pins'][pin1_index] = self.connectordef['pins'][pin2_index]
        self.connectordef['pins'][pin2_index] = temp
        

    def importConnector(con_name, refdes):
        if con_name in Connector.connectorList:
            con = dict(Connector.connectorList[con_name])
            con['nodes'] = []
            con['refdes'] = refdes
            return con
        else:
            with open(F"connectors/{con_name}.yaml", "r") as stream:
                try:
                    Connector.connectorList[con_name] = yaml.safe_load(stream)
                    return Connector.importConnector(con_name, refdes)
                except yaml.YAMLError as exc:
                    print(exc)

