import kavaad
import time

kavaad.init()

try:
    while True:
        kavaad.read_successfully()
        time.sleep(1)
except KeyboardInterrupt:
    kavaad.cleanup()
