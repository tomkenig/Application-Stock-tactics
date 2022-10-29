# Stock tactics v0.02dev
# DONE: todo: v0.02: add worker file with retry
# DONE: todo: v0.02: create view on DB - tactics after analysis with all needed m&d
# todo: v0.02: error log catch
# todo: v0.02: test 4 workers in the same time
# todo: v0.02: add service hours for ie: old tactics delete. In worker and global conf. (!time zones)
# todo: v0.02: test, test and test
# todo: v0.02: add sql's to repo
# todo: v0.02: fix worker name: for home.pl:" defaultValue
# todo: v0.02: stock fee sucks, it is based on expected yield, not on price on price when sell (fe:
#  yield not reach, but sold after x periods)
import time


if __name__ == "__main__":
    i = 0
    while i < 99999:
        try:
            exec(open("measures_and_dimensions.py").read())
            i += 1
            print(i)
        except:
            print("waiting...")
            time.sleep(100)
            continue
