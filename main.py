from input import InputModule 
from Analyzer import Analyzer
from output import Display

if __name__ == "__main__":
    input_module = InputModule("")
    analyzer = Analyzer()
    display = Display()
    input_module.register_output_fn(analyzer.recv_data)
    analyzer.register_output_fn(display.display_data)
    display.start()
    analyzer.start()
    input_module.start()

