def tech(n: int) -> str:
    #docstrings simple
    """Return tech n times"""
    
    #docstrings
    """
    Return tech n times
    
    :param n: Number of times to print tech
    :type n: int
    :raise TypeError: If n is not an int
    :return: A string of n techs, one per line
    :rtype: str
    """
    return "tech\n" * n
        
number: int = int(input("Number of techs: "))
techs: str = tech(number)
print(techs, end="")

#docstrings are used to be able to generate documentation automatically to a PDF or webpage