class Animator:
    def __init__(self):
        self.jobs = []

    def add_jobs(self, animations, asynchronous = False):
        if asynchronous:
            self.jobs.append(animations)
        else:
            self.jobs.extend(animations)

    def play(self):
        for animation in self.jobs:
            if isinstance(animation, list):
                animation[0].update()

                if animation[0].progress == 1:
                    animation[0].finish()

                    animation.pop(0)

                    if not animation:
                        self.jobs.remove(animation)
            else:
                animation.update()

                if animation.progress == 1:
                    animation.finish()

                    self.jobs.remove(animation)

    def is_playing(self):
        return len(self.jobs) > 0

    def draw(self, screen):
        for animation in self.jobs:
            if isinstance(animation, list):
                if not animation[0].should_draw:
                    continue

                animation[0].obj.draw(screen)
            else:
                if not animation.should_draw:
                    continue

                animation.obj.draw(screen)