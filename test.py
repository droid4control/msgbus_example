#!/usr/bin/python3

from msgbus import MsgBus
from modules.logic_or import Main as Or
from modules.logic_not import Main as Not
from modules.simpletrigger import Main as SimpleTrigger
from modules.debug import Main as DebugOut

from functools import partial
import tornado.ioloop

import sys
import logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

logging.getLogger('modules.module').setLevel(logging.ERROR)
logging.getLogger('msgbus').setLevel(logging.ERROR)

msgbus = MsgBus()

"""
                                           +---------+
switch1 o--+-------------------------------+ or_lamp |
           |                               |         |
           |     +----------+  sw2_status  |         +--+---o lamp
switch2 o-----+--+ pulse_sw +------+-------+         |  |
           |  |  +----------+      |       +---------+  |
           |  |                    |                    |
           |  |                    |  +--------------+  |    +---------------+
           |  |                    +--+ debug_inputs |  +----+ debug_outputs |
           |  +-----------------------+              |    +--+               |
           +--------------------------+              |    |  +---------------+
        +-----------------------------+              |    |
        |                             +--------------+    |
        |                                                 |
        |                      +------+                   |
a1 o----+----------------------+ not1 +-------------------+---o o1
                               +------+
"""

# NOT test
Not(msgbus,
    {"id": "not1",
     "inputs": {"a1": {"state": False}},
     "output": "o1"
    })

# OR test
Or(msgbus,
    {"id": "or_lamp",
     "inputs": {"switch1": {"state": False}, "sw2_status": {"state": False}},
     "output": "lamp"
    })

# pulse switch
SimpleTrigger(msgbus,
    {"id": "pulse_sw",
     "inputs": {"switch2": {"state": False}},
     "output": {"sw2_status": False}
    })

DebugOut(msgbus,
    {"id": "debug_inputs",
     "inputs": {"a1": None, "switch1": None, "switch2": None},
    })

DebugOut(msgbus,
    {"id": "debug_outputs",
     "inputs": {"o1": None, "lamp": None},
    })

# Test flows
log.info("test NOT module")
log.info("a1 on")
tornado.ioloop.IOLoop.instance().run_sync(partial(msgbus.publish, "a1", {"value": True}))
log.info("a1 on")
tornado.ioloop.IOLoop.instance().run_sync(partial(msgbus.publish, "a1", {"value": True}))
log.info("a1 off")
tornado.ioloop.IOLoop.instance().run_sync(partial(msgbus.publish, "a1", {"value": False}))
log.info("a1 off")
tornado.ioloop.IOLoop.instance().run_sync(partial(msgbus.publish, "a1", {"value": False}))

log.info("test ON/OFF switch")
log.info("switch1 ON")
tornado.ioloop.IOLoop.instance().run_sync(partial(msgbus.publish, "switch1", {"value": True}))
log.info("switch1 still ON")
tornado.ioloop.IOLoop.instance().run_sync(partial(msgbus.publish, "switch1", {"value": True}))
log.info("switch1 OFF")
tornado.ioloop.IOLoop.instance().run_sync(partial(msgbus.publish, "switch1", {"value": False}))

log.info("test pulse switch")
log.info("switch2 ON")
tornado.ioloop.IOLoop.instance().run_sync(partial(msgbus.publish, "switch2", {"value": True}))
log.info("switch2 OFF")
tornado.ioloop.IOLoop.instance().run_sync(partial(msgbus.publish, "switch2", {"value": False}))
log.info("switch2 ON")
tornado.ioloop.IOLoop.instance().run_sync(partial(msgbus.publish, "switch2", {"value": True}))
log.info("switch2 OFF")
tornado.ioloop.IOLoop.instance().run_sync(partial(msgbus.publish, "switch2", {"value": False}))
log.info("switch2 ON")
tornado.ioloop.IOLoop.instance().run_sync(partial(msgbus.publish, "switch2", {"value": True}))
log.info("switch2 OFF")
tornado.ioloop.IOLoop.instance().run_sync(partial(msgbus.publish, "switch2", {"value": False}))
