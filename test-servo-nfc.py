import kavaad as kv
import time


kv.init()

try:
    while True:
        # if kv.nfc_read() != "NO INPUT":
        #     kv.read_successfully()
        #     kv.flush_nfc()
        #     # time.sleep(0.1)
        #     # kv.flush_nfc()
        #     time.sleep(5)
        # time.sleep(1)

        kv.nfc_read()
        time.sleep(1)
    kv.cleanup()

except KeyboardInterrupt:
    kv.cleanup()
