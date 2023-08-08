import kavaad

kavaad.init()

try:
    while True:
        kavaad.speaking(1)
except KeyboardInterrupt:
    kavaad.cleanup()
