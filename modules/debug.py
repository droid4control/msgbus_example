from modules.module import Module

import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class Main(Module):
    def _oninput(self, nodeid, inp, data):
        log.debug("nodeid=%s, input=%s, data=%s", nodeid, inp, str(data))
