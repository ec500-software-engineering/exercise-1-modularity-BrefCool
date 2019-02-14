import random
import copy
from time import gmtime, strftime

global_format = {'user_id': 1,
                 'age': 24,
                 'gender': 'male',
                 'heartrate': 0,
                 'Systolic_BP': 0,
                 'Diastolic_BP': 0,
                 'blood_oxygen': 0,
                 'temperature': 0,
                 'time': ''}

def generate_rnd_data():
    new_data = copy.deepcopy(global_format)
    new_data['heartrate'] = random.random() * 100
    random_BP = [random.random()*100, random.random()*100]
    new_data['Systolic_BP'] = max(random_BP)
    new_data['Diastolic_BP'] = min(random_BP)
    new_data['blood_oxygen'] = random.random() * 100
    if random.random() >= 0.5:
        new_data['temperature'] = 37.5 + random.random()
    else:
        new_data['temperature'] = 37.5 - random.random()
    new_data['time'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return new_data