from src.data import easings
from src.engine import assets

class Animation:
    def __init__(self, obj, destination, duration_s: float = 0.5, easing: str = 'in_out_cubic', on_finish = None):
        self.obj = obj

        self.starting_x, self.starting_y = self.obj.pos
        self.destination_x, self.destination_y = destination
        
        self.duration_s = duration_s
        self.easing = easings.functions[easing]

        self.on_finish = on_finish

        self.progress = 0

    def update(self):
        easing_progress = self.easing(self.progress)

        self.obj.pos = (
            self.starting_x + ((self.destination_x - self.starting_x) * easing_progress), 
            self.starting_y + ((self.destination_y - self.starting_y) * easing_progress)
        )

        self.progress += 1 / (assets.settings['fps'] * self.duration_s)

        if self.progress >= 1:
            self.progress = 1

    def finish(self):
        if self.on_finish:
            self.on_finish()