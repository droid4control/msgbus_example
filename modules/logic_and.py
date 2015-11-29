from modules.module import Module

class Main(Module):
    def _oninput(self, nodeid, input, data):
        data['value'] = not data['value']
        self.msgbus.publish(self.output, data)

