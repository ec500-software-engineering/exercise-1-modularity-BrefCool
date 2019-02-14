import random
import time
from threading import Thread
from generator import generate_rnd_data

class InputModule(Thread):
    def __init__(self, input_file):
        Thread.__init__(self)
        self.src_file = input_file
        self.output_fn = None
    
    def register_output_fn(self, output_fn):
        self.output_fn = output_fn

    def run(self):
        print("[InputModule]start working")
        while True:
            if self.output_fn is not None:
                print("[InputModule]put data to analyzer")
                self.output_fn(generate_rnd_data())
                time.sleep(random.random()*10)
