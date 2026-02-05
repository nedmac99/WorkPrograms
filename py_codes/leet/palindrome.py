def isPalindrome(self, nums):

    #Converts the nums variable to a string
    num_str = str(nums)

    #Returns a boolean True or false if the string num_str is equal to the reverse of num_str
    return num_str == num_str[::-1]