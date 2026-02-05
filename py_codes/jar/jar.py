class Jar:
    def __init__(self, capacity=12):
        if capacity < 0 or capacity > 12:
            raise ValueError("Invalid Capacity")
        self.capacity = capacity

    def __str__(self):
        return f"{self.size} Cookies in the Jar"

    def deposit(self, n):
        if n > self.size:
            raise ValueError("Too many cookies in the jar")
        self.size += n

    def withdraw(self, n):
        if n > self.size:
            raise ValueError("Not enough cookies to remove")
        self.size -= n

    @property
    def capacity(self):
        return f"{self.capcity} spaces left for cookies"

    @property
    def size(self):
        return f"{self.size} cookies in the jar"
