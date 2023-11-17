import kavaad as kv
import time

kv.init()

try:
    while True:
        kv.speaking(1)
        time.sleep(0.2)

except KeyboardInterrupt:
    kv.cleanup()
