from src.data import easings

class Animation:
    def __init__(self, obj, destination, easing: str):
        self.obj = obj

        #self.starting_pos 
        self.x_destination, self.y_destination = destination
        
        self.easing = easings.functions[easing]