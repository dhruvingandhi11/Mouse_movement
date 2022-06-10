import time

starttime = time.time()
while True:
    print("tick")
    time.sleep(0.033 - ((time.time() - starttime) % 0.033))