# Stock tactics v0.02dev
# DONE: todo: v0.02: add worker file with retry
# DONE: todo: v0.02: create view on DB - tactics after analysis with all needend m&d
# todo: v0.02: error log catch
# todo: v0.02: test 4 workers in the same time
# todo: v0.02: add service hours for ie: old tactics delete. In worker and global conf. (!time zones)
# todo: v0.02: test, test and test

import time


if __name__ == "__main__":
    i = 0
    while i < 99999:
        try:
            exec(open("measures_and_dimensions.py").read())
            i+=1
            print(i)
        except:
            time.sleep(10)
            print("waiting...")
            continue
