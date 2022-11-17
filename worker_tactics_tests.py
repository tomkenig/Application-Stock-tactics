# Stock tactics v0.02dev
# DONE: todo: v0.02: add worker file with retry
# DONE: todo: v0.02: create view on DB - tactics after analysis with all needed m&d
# todo: v0.02: error log catch
# todo: v0.02: test 4 workers in the same time
# todo: v0.02: add service hours for ie: old tactics delete. In worker and global conf. (!time zones)
# todo: v0.02: test, test and test
# todo: v0.02: add sql's to repo
# todo: v0.02: fix worker name: for home.pl:" defaultValue as hostname
# todo: v0.02: stock fee sucks, it is based on expected yield, not on price on price when sell (fe:
#  yield not reach, but sold after x periods)
# todo: v0.02: better woprkers queue - worker wait, when other worker are updating record status pool omn start
# todo: v0.02: how many workers are optimal number for current machine - can bee calculated as done similar operations/second,
# todo: v0.02: application performance: less print and others
# todo: v0.02: BUG: same tactics generated in same time < need to be fix immediately. Only one worker can generate tactics list in one time
# todo: v0.02: New worker idea: run every 5 minutes. If process active, then exit. Process active - there are any record updated in tactics in last 5 min.
# maybee worker keep-alive is a good idea
# todo: v0.02: add new indicator :earn per signal
# todo: v0.02: round results in result string - less space
# todo: v0.02: RSI test sux - values are x 100
# todo: v0.02: when there is a flock, maybe worker... is not neccesary?
import time

if __name__ == "__main__":
    i = 0
    while i < 99999:
        try:
            print("You can quit in the next 5 seconds...")
            time.sleep(5)
            exec(open("measures_and_dimensions.py").read())
            i += 1
            print(i)
        except:
            print("waiting...")
            time.sleep(10)
            continue
