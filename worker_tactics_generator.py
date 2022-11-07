# Stock tactics v0.02dev
# todo: v0.02dev: add sleep parameters to global config file
# todo: v0.02dev: smth goeas wronk - there are more than one active processes. Process are not automaticly closed after new start
# todo: v0.02dev: DELETE THIS GENERATOR - not needed
import time
import datetime


if __name__ == "__main__":
    print("start)")
    i = 0
    while i < 99999:
        try:
            exec(open("tactic_generator.py").read())
            i+=1
            print(i)
        except:
            time.sleep(600)
            print("waiting...")
            continue
