# handle errors and logs errors to a text file
# todo: log into file
# todo: get error message
# todo: convert to dict

import os
import sys
import datetime


def errhandler_print_log():
    er_msg = "An error occured"
    er_machine = os.getenv('COMPUTERNAME', 'defaultValue')
    er_datetime = str(datetime.datetime.now())
    er_file = os.path.basename(sys.argv[0])
    return er_msg, er_machine, er_datetime, er_file


def errhandler_exit():
    exit()


if __name__ == "__main__":
    errhandler_exit()
    print(errhandler_print_log())
