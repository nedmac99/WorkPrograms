workers = [
    {"name": "Camden", "house": "Rome"},
    {"name": "TJ", "house": "Rome"},
    {"name": "Geo", "house": "Cartersville"},
    {"name": "Brandy", "house": "Cartersville"}
]


romans = filter(lambda w: w["house"] == "Rome", workers)

print("The Romans are: ")
for worker in sorted(romans, key=lambda w: w["name"]):
    print(worker["name"])