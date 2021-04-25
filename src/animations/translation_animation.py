from src.animations import Animation

class TranslationAnimation(Animation):
    def __init__(self, obj, destination, duration_s: float = 0.5, easing: str = 'in_out_cubic', should_draw: bool = True, on_finish = None):
        super().__init__(obj, duration_s, easing, should_draw, on_finish)

        self.starting_x, self.starting_y = self.obj.pos
        self.destination_x, self.destination_y = destination

    def update(self):
        easing_progress = self.easing(self.progress)

        self.obj.pos = (
            self.starting_x + ((self.destination_x - self.starting_x) * easing_progress), 
            self.starting_y + ((self.destination_y - self.starting_y) * easing_progress)
        )
        
        super().update()
    
    def finish(self):
        self.obj.pos = (
            self.destination_x,
            self.destination_y
        )

        super().finish()