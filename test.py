#!/usr/bin/python3

from msgbus import MsgBus
from modules.logic_not import Main as Not
from modules.debug import Main as DebugOut

import sys
import logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

logging.getLogger('msgbus').setLevel(logging.ERROR)

msgbus = MsgBus()

Not(msgbus,
    {"id": "not1",
     "inputs": {"a1": {"state": False}},
     "output": "o1"})

DebugOut(msgbus,
    {"id": "debug",
        "inputs": {"a1": None, "o1": None},
    })

msgbus.publish("a1", {"value": True})

