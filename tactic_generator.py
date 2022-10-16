# todo: there are no need to be more than one representation of buy_indictator_functions in set and db
# todo: save number of tactic group ID in tactics table also
# todo: correct tactic group id
# todo: correct buy_indicator_1_functions - take them from tactic_groups table
# todo: yield expectes as variable
# todo: md5 hash on json with variables
# todo: need to be equal as m&d names
# todo: IDEA: TACTCS DATA CAN BE GENERATED IN MEMORY FROM SQL VIEW OR SCRIPT. tHERE IS NO NEED TO INSERT TACTICS INTO DB
# todo: error handling ex: list out of range where there aren't any groups to handle
# todo: in m&d get function from tactics
# libs
from db_works import db_connect
import itertools
import measures_and_dimensions as md
import json
import hashlib as hl

# todo: get tactic group, make vars and change status to 1 after in progress. After all change staus to 2
def get_tactics_group_json():
    cursor.execute("SELECT tactic_group_id, tactic_group_data "
                   "FROM " + db_tactics_schema_name + "." + db_tactics_groups_table_name + " "
                   " where tactic_group_status_id = 0 order by tactic_group_id limit 1; ")
    tactics_group_data = cursor.fetchall()
    # todo: update status after select!
    cursor.execute("UPDATE " + db_tactics_schema_name + "." + db_tactics_groups_table_name + " "
                   " SET tactic_group_status_id = 1 WHERE tactic_group_id = " + str(tactics_group_data[0][0]) + "; ")
    cnxn.commit()
    tactics_group_data_json = json.loads(tactics_group_data[0][1])
    tactics_group_id = tactics_group_data[0][0]
    return tactics_group_data_json, tactics_group_id


if __name__ == "__main__":
    # get configuration
    db_klines_schema_name, db_tactics_schema_name, db_klines_anl_table_name, db_binance_settings_table_name, db_tactics_table_name, db_tactics_groups_table_name \
        , db_tactics_analyse_table_name, db_tactics_results_table_name, TMP_DIR_PATH, TACTICS_PACK_SIZE = md.get_settings_json()
    cursor, cnxn = db_connect()

    tactics_group_data_json, tactics_group_id = get_tactics_group_json()


    # todo: you car remove var creation later. It can be in the next step, while creating crosslists


    # tactic group insert
    # tactic_group_id = 1
    #tactic_group_name = tactics_group_data_json[""]
    #tactic_group_stock_tactics_version = '0.01'

    # todo: insert also tactic group id
    # todo: dont insert functions name from tactic group
    # tactics insert
    x = []
    crosslists = [tactics_group_data_json["download_settings_id"],
                  tactics_group_data_json["test_stake"],
                  tactics_group_data_json["buy_indicator_1_name"],
                  tactics_group_data_json["buy_indicator_1_value"],
                  tactics_group_data_json["buy_indicator_1_operator"],
                  tactics_group_data_json["buy_indicator_1_functions"],
                  tactics_group_data_json["yield_expected"],
                  tactics_group_data_json["wait_periods"]]

    for element in itertools.product(*crosslists):
        x.append(element)
        # print(element)

    print(len(x))

    for y in x:
        cursor.execute("INSERT INTO " + db_tactics_schema_name + "." + db_tactics_table_name + " ( download_settings_id, test_stake, buy_indicator_1_name, buy_indicator_1_value,buy_indicator_1_operator, "
                                              "buy_indicator_1_functions, yield_expected, wait_periods, stock_fee, tactic_status_id, tactic_group_id)  values "
                                              "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",  (y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7], 0.002, 0, tactics_group_id))
        print(y)

    print("insert done")
    cnxn.commit()

