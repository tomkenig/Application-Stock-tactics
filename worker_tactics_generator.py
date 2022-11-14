# Stock tactics v0.02dev
# DONE: todo: v0.02dev: add sleep parameters to global config file. Aadd also 23 hours
# DONE: todo: v0.02dev: smth. goes wrong - Process are not automaticly closed after new start
# DONE: todo: v0.02dev: will be exist. DELETE THIS GENERATOR - not needed
import time
from datetime import datetime, timedelta
import measures_and_dimensions as md


if __name__ == "__main__":
    db_klines_schema_name, db_tactics_schema_name, db_klines_anl_table_name, db_binance_settings_table_name, \
    db_tactics_table_name, db_tactics_groups_table_name, db_tactics_analyse_table_name, \
    db_tactics_results_table_name, db_tactics_workers_table_name, TMP_DIR_PATH, TACTICS_PACK_SIZE, \
    worker_tactics_generator_work_hours, worker_tactics_generator_sleep = md.get_settings_json()

    print(worker_tactics_generator_work_hours)
    print(worker_tactics_generator_sleep)

    end_date = datetime.strptime(str(datetime.now() + timedelta(hours=worker_tactics_generator_work_hours))[0:16], "%Y-%m-%d %H:%M")
    print("start worker)")
    while datetime.strptime(str(datetime.now())[0:16], "%Y-%m-%d %H:%M") < end_date:
        try:
            exec(open("tactic_generator.py").read())
        except:
            time.sleep(worker_tactics_generator_sleep)
            print("waiting...")
            continue
