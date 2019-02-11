import time
import sys
import os

sys.path.append(os.getcwd())

from input_api import input_api
from Analyzer import Analyzer
from OutputAlert_module import receive_basic_iuput_data
from Database_Module import DataBaseModule

if __name__ == "__main__":
    simulate_data = [[1, 24, 'male', 100, 75, 125, 71, 36, '2019-02-10 13:31:22'],
                     [1, 24, 'male', 110, 77, 123, 69, 37, '2019-02-10 13:31:23'],
                     [1, 24, 'male', 123, 89, 100, 80, 38, '2019-02-10 13:31:24']]
    username = 'admin'
    password = '123456'
    
    for data in simulate_data:
        # get input data
        data_obj = input_api(data[0], data[1], data[2], data[3], data[4], data[5],
                             data[6], data[7], data[8])
        data_obj.implement_filter()
        data_dict_for_alert = data_obj.return_request(1)
        uid, data_dict_for_db = data_obj.return_request(2)
        # save into database
        db_mng = DataBaseModule()
        db_mng.authen(username, password)
        db_mng.insert(uid, data_dict_for_db)
        # analyse the data
        analyzer = Analyzer(data_dict_for_alert['Systolic_BP'],
                            data_dict_for_alert['Diastolic_BP'],
                            data_dict_for_alert['heartrate'],
                            data_dict_for_alert['blood_oxygen'],
                            data_dict_for_alert['temperature'])
        signal_loss = analyzer.Signal_Loss(data_dict_for_alert['heartrate'],
                                           data_dict_for_alert['temperature'])
        shock_alert = analyzer.Shock_Alert(data_dict_for_alert['heartrate'],
                                           data_dict_for_alert['temperature'])
        oxygen_supply = analyzer.Oxygen_Supply(data_dict_for_alert['blood_oxygen'])
        fever = analyzer.Fever(data_dict_for_alert['temperature'])
        hypotension = analyzer.Hypotension(data_dict_for_alert['Systolic_BP'], data_dict_for_alert['Diastolic_BP'])
        hypertension = analyzer.Hypertension(data_dict_for_alert['Systolic_BP'], data_dict_for_alert['Diastolic_BP'])
        # get analyse result
        result = receive_basic_iuput_data(signal_loss, shock_alert, oxygen_supply, \
            fever, hypotension, hypertension)
        print("current patient's status:")
        print(data_dict_for_alert)
        print("analyse result:")
        print(result)
        
        time.sleep(2)
        