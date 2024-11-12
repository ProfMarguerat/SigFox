#!/usr/bin/env python

import time

from envirophat import weather, leds


print("""Light the LEDs upon temperature increase.
Press Ctrl+C to exit.
""")
leds.on()

threshold = 0

try:
    while True:
        temperature = weather.temperature()

        #if threshold is None:
            #threshold = temperature + 0.001

        print("{} degrees Celsius".format(temperature))
        if temperature > threshold:
            leds.on()
        else:
            leds.off()

        time.sleep(0.5)

        threshold = temperature + 0.001

except KeyboardInterrupt:
    pass
