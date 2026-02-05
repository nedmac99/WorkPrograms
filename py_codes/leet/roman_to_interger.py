def roman_num_to_integer(roman_num):
    #Store roman numerals intoa dictionary so we can use key and value pairs to get value using roman numeral key
    romans = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000
    }
    
    #Number we intend to return as integer
    number = 0
    
    #Created 3 seperate replace instances for readability instead of doing 6 individual replacements or 1 long one 
    roman_num = roman_num.replace("IV", "IIII").replace("IX", "VIIII")
    roman_num = roman_num.replace("XL", "XXXX").replace("XC", "LXXXX")
    roman_num = roman_num.replace("CD", "CCCC").replace("CM", "DCCC")
    
    #Loops through each character in the roman_num string and adds the value to variable number
    for char in roman_num:
        number += romans[char]
        
    #Returns number value    
    return number
