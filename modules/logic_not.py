from modules.module import Module

import copy

class Main(Module):
    def _oninput(self, nodeid, input, data):
        newdata = data
        newdata['value'] = not data['value']
        self.msgbus.publish(self.output, newdata)
