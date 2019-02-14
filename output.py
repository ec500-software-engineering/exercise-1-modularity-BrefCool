from threading import Thread
from queue import Queue

class Display(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.output_queue = Queue()
    
    def display_data(self, data):
        self.output_queue.put(data)

    def run(self):
        while True:
            data = self.output_queue.get()
            print(data['info'])
            alerts = data['alert']
            alert_info = ""
            for key in alerts.keys():
                if alerts[key]:
                    alert_info += (key + " ")
            print(alert_info)