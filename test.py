import kavaad as kv
import time

kv.init()

try:
    while True:
        # print(kv.check_next_botton(-1))
        print(kv.check_next_botton(-2))
        print(kv.check_next_botton(-3))
        print()
        time.sleep(1)
except KeyboardInterrupt:
    kv.cleanup()
