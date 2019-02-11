# fork from https://github.com/leonshen95/EC500-Modular-design-2.4/blob/master/AI%20module.py
import numpy as np
from Database_Module import DataBaseModule
# Input: ID(from main function perhaps), infoDB(from Database function)
# output: Three predicted parameters, three Alert signals(Type:Boolean

class AI_module(object):
    def __init__(self, dict):
        self._dict = dict

    def Query_Data_From_Database(self,ID,infoDB):
        ## connect database, query previous one day data from Database
        # Database = database_dict()
        Blood_oxygen = []
        Blood_pressure = []
        Pulses = []
        
        info = DataBaseModule().search(ID)
        # Username = input("")
        #get dictionary from database
        for key in infoDB:
            if key== ID:
                pressure = info['blood_pressure']
                oxygen = info['blood_oxygen']
                Pulse = info['blood_pulses']
                Blood_pressure.append(pressure)
                Blood_oxygen.append(oxygen)
                Pulses.append(Pulse)


        return Blood_oxygen, Blood_pressure, Pulses


    def AI_Module(self,Blood_oxygen, Blood_pressure, Pulses):

        ## AI module do the prediection, The AI module uses previous data
        oxygen=np.array(Blood_oxygen)
        pressure = np.array(Blood_pressure)
        Pulse = np.array(Pulses)
        pressure_predict_result = np.mean(pressure)
        oxygen_predict_result=np.mean(oxygen)
        Pulse_predict_result = np.mean(Pulse)

        return pressure_predict_result, oxygen_predict_result, Pulse_predict_result


    def Feedback(self,Blood_pressure_predict_result, Blood_oxygen_predict_result, Pulse_predict_result):
        lower_BP= 80
        upper_BP= 120
        lower_BO = 80
        upper_BO = 120
        lower_Pulse = 80
        upper_Pulse = 120
        BP_Alert= False
        BO_Alert = False

        Pulse_Alert =False
        if(Blood_oxygen_predict_result<lower_BO or Blood_oxygen_predict_result>upper_BO):
            BO_Alert =True
        if(Blood_pressure_predict_result<lower_BP or Blood_pressure_predict_result>upper_BP):
            BP_Alert =True
        if(Pulse_predict_result< lower_Pulse or Pulse_predict_result >upper_Pulse):
            Pulse_Alert =True
        ## feedback the AI prediction restult to the interface
        ## It will turn on the Alert when the statues get worse.
        return BO_Alert,BP_Alert,Pulse_Alert


