import numpy as np
import matplotlib.pyplot as plt

#Objectives
'''
-Simulate rolling two dice 10,000 times
-Calculate the sum of each roll (which will range from 2 to 12)
-Analyze and count how often each sum appears
-Compare the results to theoretical probabilities (e.g., 7 is the most common sum)
'''

#initialize a number of rolls and then roll 2 dice that many times
num_of_rolls = 10000
rolls = np.random.randint(1, 7, size=(num_of_rolls, 2))
#print(rolls)

#Compute the sum of each roll and show the first 10 results
sums = np.sum(rolls, axis=1)
#print(sums[:10])

#Count how often each total appears
unique_sums, counts = np.unique(sums, return_counts=True)
#print(unique_sums.sum())

#Display results neatly
for value, count in zip(unique_sums, counts):
    print(f"Sum {value} appears {count} times")
    
plt.bar(unique_sums, counts)
plt.title("Dice Sum Probabilities")
plt.xlabel("Unique Sums")
plt.ylabel("Times it was hit")
plt.grid(visible=True, axis='y')
plt.show()