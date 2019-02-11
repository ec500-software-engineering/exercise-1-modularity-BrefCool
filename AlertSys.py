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
                     [1, 24, 'male', 55, 89, 100, 80, 28, '2019-02-10 13:31:24'],
                     [1, 24, 'male', 145, 56, 89, 111, 37, '2019-02-10 13:31:25'],
                     [1, 24, 'male', 200, 22, 220, 80, 40, '2019-02-10 13:31:26'],
                     [1, 24, 'male', 50, 56, 88, 22, 35, '2019-02-10 13:31:27'],
                     [1, 24, 'male', 175, 77, 33, 98, 38, '2019-02-10 13:31:28'],
                     [1, 24, 'male', 115, 224, 990, 56, 37, '2019-02-10 13:31:29'],
                     [1, 24, 'male', 87, 89, 103, 80, 38, '2019-02-10 13:31:30'],
                     [1, 24, 'male', 111, 67, 134, 78, 37, '2019-02-10 13:31:31'],
                     [1, 24, 'male', 134, 89, 120, 90, 38, '2019-02-10 13:31:32'],
                     [1, 24, 'male', 189, 60, 887, 45, 37, '2019-02-10 13:31:33'],
                     [1, 24, 'male', 66, 819, 33, 80, 38, '2019-02-10 13:31:34'],
                     [1, 24, 'male', 110, 77, 123, 100, 37, '2019-02-10 13:31:35'],
                     [1, 24, 'male', 89, 89, 34, 80, 38, '2019-02-10 13:31:36']]
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
        
        time.sleep(1)
        