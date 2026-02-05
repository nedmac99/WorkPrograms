class Person:
    def __init__(self, name, house):
        if not name:
            raise ValueError("Missing Name")
        self.name = name
        self.house = house

    def __str__(self):
        return f"{self.name} from {self.house}"

    @property
    def house(self):
        return self._house

    @house.setter
    def house(self, house):
        if house not in ["Rome", "Cartersville"]:
            raise ValueError("Invalid House")
        self._house = house


def main():
    person = get_person()
    print(person)


def get_person():
    name = input("Name: ")
    while True:
        house = input("House: ")
        try:
            return Person(name, house)
        except ValueError as e:
            print(e)
        return Person(name, house)


if __name__ == "__main__":
    main()
