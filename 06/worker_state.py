class WorkerState:
    def __init__(self, state: bool):
        self.state = state

    def is_on(self):
        return self.state

    def turn_on(self):
        self.state = True

    def turn_off(self):
        self.state = False
