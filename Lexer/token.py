class Token:
    def __init__(self, type: int, value, position: tuple = (0, 0)):
        self.type = type
        self.value = value
        self.position = position

    def __repr__(self):
        return f"Token: {self.type}, {self.value}"