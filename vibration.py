#!/usr/bin/env python
import sys
import os
import time
import logging
import threading
import json
import RPi.GPIO as GPIO
import requests

def send_appliance_active_message():
    # For our purposes, this is basically a no-op. You can add more here though
    logging.info("The Appliance Monitor is active!")
    global appliance_active
    appliance_active = True

def send_appliance_inactive_message():
    logging.info("The Appliance Monitor has sensed completion")
    global appliance_active
    appliance_active = False
    # After the appliance starts, THEN send a page when the appliance stops
    # Define the payload
    # https://v2.developer.pagerduty.com/v2/docs/send-an-event-events-api-v2
    payload = {
        "event_action": "trigger",
        "payload": {
            "summary": "The laundry is done!",
            "severity": "info",
            "source": "rpi",
            }
        }
    payload['routing_key'] = str(os.environ['PD_SERVICE_KEY'])

    # Trigger an event
    r = requests.post('https://events.pagerduty.com/v2/enqueue',
            data=json.dumps(payload))
    logging.debug(r.json())

def vibrated(x):
    global vibrating
    global last_vibration_time
    global start_vibration_time
    logging.debug('Vibrated')
    last_vibration_time = time.time()
    if not vibrating:
        start_vibration_time = last_vibration_time
        vibrating = True

def heartbeat():
    current_time = time.time()
    logging.debug("Heartbeat ran at {}".format(current_time))
    global vibrating
    delta_vibration = last_vibration_time - start_vibration_time
    if (vibrating and delta_vibration > begin_seconds
            and not appliance_active):
        send_appliance_active_message()
    if (not vibrating and appliance_active
            and current_time - last_vibration_time > end_seconds):
        send_appliance_inactive_message()
    # False if it has been 2 seconds since vibration
    vibrating = current_time - last_vibration_time < 2
    threading.Timer(1, heartbeat).start()

logging.basicConfig(format='%(message)s', level=logging.INFO)

vibrating = False
appliance_active = False
last_vibration_time = time.time()
start_vibration_time = last_vibration_time

verbose = os.getenv('VERBOSE', False)
sensor_pin = 14
begin_seconds = 180 # attempt to sense 2 minutes of vibration before starting
end_seconds = 60    # attempt to sense 1 minutes of being stopped before paging

if verbose:
    logging.getLogger().setLevel(logging.DEBUG)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(sensor_pin, GPIO.RISING)
GPIO.add_event_callback(sensor_pin, vibrated)

logging.info('monitoring GPIO pin {}'.format(str(sensor_pin)))
threading.Timer(1, heartbeat).start()
