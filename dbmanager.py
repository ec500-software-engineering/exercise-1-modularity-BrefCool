# fork from https://github.com/leonshen95/EC500-Modular-design-2.4/blob/master/Database_Module.py
authenDB = {'admin':"123456"}
infoDB = {}

"""
data format of infoDB:
{
    'XXXXXX(user_id)': [{
        'time': '2019-02-06 17:11',
        'gender': 'male',
        'heartrate': 100,
        'blood_pressure': 125,
        'blood_oxygen': 0.7
        },
        {
            ...
        }
    ]
}
"""

def authen(username, password):
    """
    user log in, must call this function before using delete\insert\search 
    :param username: user id
    :param password: user password
    :return void
    """
    if authenDB[username] == password:
        return True
    else:
        return False


def delete(ID):
    """
    delete patient's data based on user id
    :param ID: user id
    :return void
    """
    infoDB.popitem(ID)

    
def insert(ID,info):
    infoDB[ID] = info
            
    
def search(ID):
    return infoDB[ID]