class Animator:
    def __init__(self):
        self.jobs = []

    def add_to_jobs(self, animations, asynchronous = False, on_finish = None):
        if asynchronous:
            self.jobs.append(animations)
        else:
            self.jobs.extend(animations)

    def play(self):
        for animation in self.jobs:
            if isinstance(animation, list):
                animation = animation[0]
                
            animation.update()
