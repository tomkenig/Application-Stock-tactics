# handle errors and logs errors to a text file
# DONE: todo: log into file
# DONE: todo: get error message
# DONE: todo: convert to dict
# DONE: todo: create log directory
# todo: v0.02: use also logging library

# Stock tactics v0.01

import os
import sys
import datetime
import json

# print and save log as a json file
def errhandler_log(exception_in):
    # create temporary directory for error logs
    try:
        os.mkdir("error_logs")
    except OSError as error:
        print(error)

    #err_log = {}
    err_msg = str(exception_in)
    err_machine = str(os.getenv('COMPUTERNAME', 'defaultValue'))
    err_datetime = str(datetime.datetime.now())
    err_file = str(os.path.basename(sys.argv[0]))
    print(err_msg, err_machine, err_datetime, err_file)
    err_log = json.dumps(dict(zip(('err_msg', 'err_machine', 'err_datetime', 'err_file'),
                                  (err_msg, err_machine, err_datetime, err_file))))
    with open("error_logs/" + err_datetime.replace(':', '.') + '_' + err_machine + ".log", 'w', encoding='utf8') as f:
        json.dump(err_log, f)
    return print(err_log), exit()

#try:
#    'ASD' * [2314.1]
#except Exception as e:
#    errhandler_log(e)
