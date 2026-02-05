workers = [
{"name": "Camden", "house": "Rome"},
{"name": "TJ", "house": "Rome"},
{"name": "Geo", "house": "Cartersville"},
{"name": "Brandy", "house": "Cartersville"}
]

heros = [
    worker["name"] for worker in workers if worker["house"] == "Rome"
]
villians = [
    worker["name"] for worker in workers if worker["house"] == "Cartersville"
]

def main():
    print("Heros are: ")
    for hero in sorted(heros):
        print(hero)
    
    print("\nVillians are: ")
    for villian in sorted(villians):
        print(villian)



'''
def main():
    yell("This","is","sparta")
    
def yell(*words):
    uppercased = [word.upper() for word in words]
    print(*uppercased)
 '''
 
    
if __name__ == "__main__":
    main()