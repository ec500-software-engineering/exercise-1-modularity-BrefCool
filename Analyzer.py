import copy
from threading import Thread
from queue import Queue
from dbmanager import *

class Analyzer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.data_queue = Queue()
        self.counter = 0
        self.output_fn = None
        self.result_format = {'Signal_Loss': False, 
                              'Shock_Alert': False,
                              'Oxygen_Supply': False,
                              'Fever': False,
                              'Hypotension': False,
                              'Hypertension': False}

    def Signal_Loss(self, Heart_Rate, Body_temp):
        # Signal loss judgement
        if (Heart_Rate < 60 and Body_temp < 36):
            return True
        return False

    def Shock_Alert(self, Heart_Rate, Body_temp):
        # Shock emergency judgement
        if (Heart_Rate < 60 and Body_temp >= 36):
            return True
        return False
    
    def Oxygen_Supply(self, Heart_O2_Level):
        # Oxygen supply judgement
        if (Heart_O2_Level < 70):
            return True
        return False
    
    def Fever(self, Body_temp):
        # Fever judgement
        if (Body_temp > 37.5):
            return True
        return False
    
    def Hypotension(self, Systolic_BP, Diastolic_BP):
        # Hypotension judgement
        if (Systolic_BP < 90 and Diastolic_BP < 60):
            return True
        return False
    
    def Hypertension(self, Systolic_BP, Diastolic_BP):
        # Hypertension judgement
        if (Systolic_BP > 140 or Diastolic_BP > 90):
            return True
        return False

    def register_output_fn(self, output_fn):
        self.output_fn = output_fn

    def recv_data(self, data):
        self.data_queue.put(data)
    
    def analyse(self, data):
        result = copy.deepcopy(self.result_format)
        result['Signal_Loss'] = self.Signal_Loss(data['heartrate'], data['temperature'])
        result['Shock_Alert'] = self.Shock_Alert(data['heartrate'], data['temperature'])
        result['Oxygen_Supply'] = self.Oxygen_Supply(data['blood_oxygen'])
        result['Fever'] = self.Fever(data['temperature'])
        result['Hypotension'] = self.Hypotension(data['Systolic_BP'], data['Diastolic_BP'])
        result['Hypertension'] = self.Hypertension(data['Systolic_BP'], data['Diastolic_BP'])
        return result
    
    def save_db(self, raw_data):
        uid = raw_data['user_id']
        data = {'gender': raw_data['gender'],
                'heartrate': raw_data['heartrate'],
                'Diastolic_BP': raw_data['Diastolic_BP'],
                'Systolic_BP': raw_data['Systolic_BP'],
                'blood_oxygen': raw_data['blood_oxygen'],
                'temperature': raw_data['temperature'],
                'time': raw_data['time']}
        insert(uid, data)
    
    def run(self):
        print("[Analyzer]start working")
        while True:
            patient_data = self.data_queue.get()
            self.counter += 1
            # print(patient_data)
            result = self.analyse(patient_data)
            self.save_db(patient_data)
            if self.output_fn is not None:
                self.output_fn({'info': patient_data,
                                'alert': result})