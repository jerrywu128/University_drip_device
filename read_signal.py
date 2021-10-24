from mcp3008 import MCP3008
import time

adc = MCP3008(0, 0)

try:
    while True:
        signal = adc.read(0)
        print("Siginal: {0}".format(signal))
        time.sleep(1.105)

except KeyboardInterrupt:
    adc.close()
