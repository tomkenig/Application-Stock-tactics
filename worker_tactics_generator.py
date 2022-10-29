# Stock tactics v0.02dev

import time

if __name__ == "__main__":
    i = 0
    while i < 99999:
        try:
            exec(open("tactic_generator.py").read())
            i+=1
            print(i)
        except:
            time.sleep(1000)
            print("waiting...")
            continue
