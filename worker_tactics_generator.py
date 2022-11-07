# Stock tactics v0.02dev
# todo: v0.02dev: add sleep parameters to global config file
# todo: v0.02dev: smth goeas wronk - there are more than one active processes. Process are not automaticly closed after new start
# todo: v0.02dev: DELETE THIS GENERATOR - not needed
import time
from datetime import datetime, timedelta

end_date = datetime.strptime(str(datetime.now() + timedelta(hours=23))[0:16], "%Y-%m-%d %H:%M")

if __name__ == "__main__":
    print("start worker)")
    while datetime.strptime(str(datetime.now())[0:16], "%Y-%m-%d %H:%M") < end_date:
        try:
            exec(open("tactic_generator.py").read())
        except:
            time.sleep(600)
            print("waiting...")
            continue
