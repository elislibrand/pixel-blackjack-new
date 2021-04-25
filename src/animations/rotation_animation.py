from src.animations import Animation

class RotationAnimation(Animation):
    def __init__(self, obj, rotation, duration_s: float = 0.2, easing: str = 'in_out_cubic', should_draw: bool = True, on_finish = None):
        super().__init__(obj, duration_s, easing, should_draw, on_finish)

        self.starting_rotation_x, self.starting_rotation_y, self.starting_rotation_z = self.obj.rotation
        self.rotation_x, self.rotation_y, self.rotation_z = rotation

    def update(self):
        easing_progress = self.easing(self.progress)

        self.obj.rotation = (
            self.starting_rotation_x + ((self.rotation_x - self.starting_rotation_x) * easing_progress), 
            self.starting_rotation_y + ((self.rotation_y - self.starting_rotation_y) * easing_progress),
            self.starting_rotation_z + ((self.rotation_z - self.starting_rotation_z) * easing_progress)
        )

        self.obj.update_rotation()
        
        super().update()

    def finish(self):
        self.obj.rotation = (
            self.rotation_x,
            self.rotation_y,
            self.rotation_z
        )
        
        self.obj.update_rotation()

        super().finish()