import copy

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class Module(object):
    def __init__(self, msgbus, cfg):
        log.debug("__init__(%s, %s)", str(msgbus), str(cfg))
        self.msgbus = msgbus
        self.cfg = copy.deepcopy(cfg)
        self.inputs = {}
        self.output = None
        output = self.cfg.get("output", None)
        if isinstance(output, str):
            self.output_name = output
            self.output = {"value": None}
        elif isinstance(output, dict):
            if len(output) != 1:
                raise Exception("Only one output is possible")
            for output_name in output:
                self.output_name = output_name;
                self.output = {"value": output[output_name]}

        for input_name in self.cfg.get("inputs", {}):
            self.msgbus.subscribe(self.cfg.get("id", None), input_name, self, self._oninput)
            self.inputs[input_name] = {}
            inpcfg = self.cfg['inputs'][input_name]
            if inpcfg:
                self.inputs[input_name]['value'] = inpcfg.get("state", None)
            else:
                self.inputs[input_name]['value'] = None

    def _oninput(self, nodeid, input_name, data):
        log.debug("_oninput(%s, %s, %s)", nodeid, input_name, data)
        if self.inputs[input_name]['value'] == data['value']:
            return
        self.inputs[input_name] = data
        self._output(self._process())

    def _process(self):
        raise Exception("_process not implemented")

    def _output(self, output):
        if output['value'] != self.output['value']:
            self.output = output
            self.msgbus.publish(self.output_name, self.output)
