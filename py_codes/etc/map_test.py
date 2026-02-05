def main():
    yell("This","is","CS50")

#The asterisk(*) will unpack the values and allow us to use as many values as we need
def yell(*words):
    #The map keyword will allow us to identify a function we want to use and then an iteratable object that we want to apply the function to
    uppercased = map(str.upper, words)
    print(*uppercased)

if __name__ == "__main__":
    main()