#Constants use all uppercase by convention but are not supported by python so if you encounter an all uppercase variable, just don't change it

class Techs:
    
    NUM_OF_TECHS = 11
    
    def working(self):
        for _ in range(Techs.NUM_OF_TECHS):
            print("This tech is working")
            
tech = Techs()
tech.working()


'''
TECHS = 11

for _ in range(TECHS):
    print("Tech")
'''