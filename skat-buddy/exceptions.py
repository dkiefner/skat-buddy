class InvalidCardSize(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidPlayerMove(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
