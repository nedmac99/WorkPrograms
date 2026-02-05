def main():
    n = int(input("What's n? "))
    for s in star(n):
        print(s)
        

def star(n):
    
    for i in range(n):
        yield "*" * i


        
if __name__ == "__main__":
    main()
    