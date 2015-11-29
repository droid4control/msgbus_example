class Module(object):
    def __init__(self, msgbus, cfg):
        self.msgbus = msgbus
        self.nodeid = cfg.get("id", None)
        self.inputs = cfg.get("inputs", None)
        self.output = cfg.get("output", None)

        for inp in self.inputs:
            self.msgbus.subscribe(self.nodeid, inp, self, self._oninput)

    def _oninput(self, nodeid, input, data):
        raise Exception("_oninput not implemented")
