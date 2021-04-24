from src.data import easings
from src.engine import assets

class Animation:
    def __init__(self, obj, duration_s: float, easing: str, on_finish):
        self.obj = obj
        
        self.duration_s = duration_s
        self.easing = easings.functions[easing]

        self.on_finish = on_finish

        self.progress = 0

    def update(self):
        self.progress += 1 / (assets.settings['refresh_rate'] * self.duration_s)

        if self.progress >= 1:
            self.progress = 1
            
    def finish(self):
        if self.on_finish:
            self.on_finish()