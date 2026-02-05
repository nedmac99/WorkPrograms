people = [
    {"name": "Camden", "house": "Rome"},
    {"name": "Geo", "house": "Cartersville"},
    {"name": "TJ", "house": "Rome"},
    {"name": "Jacob", "house": "Adairsville"},
    {"name": "Ron", "house": "Florida"}
]

'''
houses = []
for person in people:
    if person["house"] not in houses:
        houses.append(person["house"])
'''
#Produces same result as above but uses set object
houses = set()
for person in people:
    houses.add(person["house"])
        
for house in sorted(houses):
    print(house)