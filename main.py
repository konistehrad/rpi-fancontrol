#!/usr/bin/env python3

import argparse
import logging
import math
import pprint
import time
import threading
import fanconfig
from gpiozero import Device, CPUTemperature, PWMLED, LED, Button

config = fanconfig.get_config()
cpu = CPUTemperature()
fanspeed = PWMLED(config.pin, True, 0, 20)
try:
    logging.info("Raspberry Pi PWM fan controller coming online")
    logging.debug(pprint.pformat(config))
    while True:
        temperature = cpu.temperature
        pair = next(
            (step for step in config.curve if temperature > step[0]), 
            config.curve[len(config.curve)-1])
        speed = pair[1]
        fanspeed.value = speed
        logging.debug(f"Assigning speed factor {speed} for temperature {temperature}")
        time.sleep(1 / config.pollrate)
except KeyboardInterrupt as e:
    pass
finally:
    fanspeed.value = 0
