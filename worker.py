# Stock tactics v0.02dev
# todo: v0.02: add worker file
# todo: v0.02: log catch
# todo: v0.02: test 4 workers in the same time
# todo: v0.02: add service hours for ie: old tactics delete
# todo: v0.02: view - tactics after analysis with all needend m&d

import time


if __name__ == "__main__":
    try:
        i = 0
        while i < 9999:
            print("iteration number: ", i)
            exec(open("measures_and_dimensions.py").read())
            i += 1
            time.sleep(5)
    except:
        # sleep and retry
        time.sleep(100)
        pass
