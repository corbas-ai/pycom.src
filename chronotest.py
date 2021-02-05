from machine import Timer
import time

chrono = Timer.Chrono()

chrono.start()
time.sleep(1.25)
lap = chrono.read()
time.sleep(1.5)
chrono.stop()
total = chrono.read()

print()
print("\n racer took %f seconds to finish"%total)
print("  %f seconds in the first lap"%lap)
print("  %f seconds in the last lap"%(total-lap))
