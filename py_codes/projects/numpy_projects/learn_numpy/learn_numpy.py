import numpy as np

#Create a 1-Dimensional Array and print out it's dimmension.

#arr = np.array([10, 20, 30, 40, 50])
#print(arr.ndim)
#Result = 1

#Create a 2-Dimensional Array and print out the array and it's dimmension.

#arr2 = np.array([[5, 10, 15], [20, 25, 30]])
#print(arr2)
#print(arr2.ndim)
#Result = [[5, 10, 15], [20, 25, 30]] and 2

#Check the shape and size of the 2 dimmensional array (arr2).

#print(arr2.shape)
#print(arr2.size)
#Result = (2, 3) for 2 rows and 3 columns and 6 for a count of how many elements there are

'''
np.zeors(shape) creates array Filles with zeros. Ex. np.zeros((2, 3))
np.ones(shape) creates array Filles with ones. Ex. np.ones((2, 3))
np.full(shape) creates array Filles with custom value. Ex. np.full((2, 3), 9)
np.arange(start, stop, step) Like Python range(). Ex. np.arange(0, 10, 2)
np.linspace(start, stop, num) Evenly spaced values. Ex. np.linspace(0, 1, 5)

'''

#Create 3x3 array filled with the number 7 using np.full() and print array
#arr = np.full((3, 3), 7) #((rows, columns), value)
#print(arr)

'''
np.random.rand(rows, cols) → random floats [0, 1)
np.random.randint(low, high, size=(x, y)) → random integers
np.random.randn(rows, cols) → random numbers from a normal distribution
Ex. np.random.randint(1, 10, size=(2, 3)) This creates a 2×3 array of random integers between 1 and 9.
'''

#Create a 4x4 array of random integers between 50 and 100 (inclusive of 50, and exclusive of 100)
#arr = np.random.randint(50, 100, size=(4, 4))
#print(arr)

#Using the previous arr, print the element in the 2nd row and 3rd column
#print(arr[1, 2])

#Print the entire 1st column of the array
#print(arr[:, 0]) # : means "all rows" and 0 is the column index for the first column

#Print the last two rows and last two columns of the array
#print(arr[2:, 2:]) #2: means rows 2 to the end (i.e., last two rows) and 2: for columns means columns 2 to the end

#Element-wise math

#arr1 = np.array([1, 2, 3])
#arr2 = np.array([4, 5, 6])

#print(arr1 + arr2) #[5 7 9] Adding the two arrays
#print(arr1 * arr2) #[4 10 18] Multiplying the two arrays
#print(arr1 ** 2) #[1 4 9] Squaring the first array

#Create a 1-D array called nums with the values [2, 4, 6, 8]. Multiply by 3 and print result
#nums = np.array([2, 4, 6, 8])
#print(nums * 3)

#Element-Wise Operations Between Two Arrays
#a = np.array([1, 2, 3])
#b = np.array([10, 20, 30])

#print(a + b) # [11 22 33]
#print(a - b) # [-9 -18 -27]
#print(a * b) # [10 40 90]

#Create two arrays a and b and print the result of a / b
#a = np.array([5, 10, 15])
#b = np.array([2, 4, 6])

#print(a / b) #Result is [2.5 2.5 2.5]

#Boolean Indexing
#arr = np.array([10, 15, 20, 25])
#print(arr > 15) #Result = [False False  True  True]
#print(arr[arr > 15]) #Result = [20 25]

#Print only the scores greater than or equal to 80
#scores = np.array([72, 85, 91, 64, 77])
#print(scores[scores >= 80]) #Result = [85 91]

#Aggregate Functions
'''
Function	Description
np.sum()	Total of all elements
np.mean()	Average value
np.min()	Smallest value
np.max()	Largest value
np.std()	Standard deviation
'''
#Examples
#arr = np.array([1, 2, 3, 4])
#print(np.sum(arr))   # 10
#print(np.mean(arr))  # 2.5

#Print the average score, highest score, and, the standard deviation
#scores = np.array([72, 85, 91, 64, 77])
#print(np.mean(scores)) #Result = 77.8
#print(np.max(scores)) #Result = 91
#print(np.std(scores)) #Result = 9.495261976375375 or ~9.50

#Reshaping arrays
'''
Method	    Description
.reshape()	Changes shape without changing data
.flatten()	Converts any array into 1D
.ravel()	Like flatten() but returns a view
'''

#Example
#arr = np.array([1, 2, 3, 4, 5, 6])
#reshaped = arr.reshape((2, 3))  # 2 rows, 3 columns

#Create 1-D array, reshape it into 2x3 array, print out array
arr = np.array([1,2,3,4,5,6])
#print(arr)
arr = arr.reshape((2, 3))
#print(arr)

#Flatten the array back into a 1-D array
arr = arr.flatten()
print(arr)