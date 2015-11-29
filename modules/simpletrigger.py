from modules.module import Module

import copy

class Main(Module):
    def __init__(self, msgbus, cfg):
        super(Main, self).__init__(msgbus, cfg)
        if len(self.inputs) != 1:
            raise Exception("Only one input possible")
        self.output = self._process()

    def _process(self):
        output = copy.deepcopy(self.output)
        # reverse output during raising edge
        if self.inputs[list(self.inputs.items())[0][0]]['value']:
            output['value'] = not output['value']
        return output
