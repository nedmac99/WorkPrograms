#With a target integer in mind, iterate through a list of numbers and return the indicies of the numbers that add up to the target integer

class Solution(object):
    def twoSum(self, nums, target):
        dict = {}
        for index, value in enumerate(nums):
            compliment = target - value
            if compliment in dict:
                print([dict[compliment], index])
            dict[value] = index
        
    twoSum(None, [2,7,11,15], 9)