class Nodo:
    def __init__(self):
        self.next = None

    def set_next(self, next):
        self.next = next

    def get_next(self):
        return self.next