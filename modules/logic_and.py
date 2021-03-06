from modules.module import Module

import copy

class Main(Module):
    def __init__(self, msgbus, cfg):
        super(Main, self).__init__(msgbus, cfg)
        if not len(self.inputs):
            raise Exception("At least one input is needed")
        self.output = self._process()

    def _process(self):
        output = {}
        output['value'] = True
        for input_name in self.inputs:
            if not self.inputs[input_name]['value']:
                output['value'] = False
                break
        return output
