from modules.module import Module

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class Main(Module):
    def __init__(self, msgbus, cfg):
        super(Main, self).__init__(msgbus, cfg)
        if not len(self.inputs):
            raise Exception("At least one input is needed")
        self.output = self._process()

    def _oninput(self, nodeid, input_name, data):
        log.info("_oninput(%s, %s, %s)", nodeid, input_name, data)
        super(Main, self). _oninput(nodeid, input_name, data)

    def _process(self):
        # no output from this module
        return {"value": None}
