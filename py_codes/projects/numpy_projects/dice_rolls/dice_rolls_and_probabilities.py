import numpy as np
import matplotlib.pyplot as plt

#Objectives
'''
-Generate random dice rolls using NumPy
-Simulate 1,000+ rolls
-Analyze frequencies and basic probability
'''

#Simulate dice roll
num_of_rolls = 1000
roll = np.random.randint(1, 7, size=num_of_rolls)
#print(roll) #To preview the first 10 print(roll[:10])

#Create array of unique values and how many times that value appears
unique, count = np.unique(roll, return_counts=True)
#print(f"Unique number: {unique}")
#print(f"Count of number: {count}")

#Calculate probability (count of that number) / (total rolls)
prob = (count / num_of_rolls) #Or (count / count.sum())
#print(f"Probability of each number: {prob}")

#Loops through the 6 different values and printed out the probability of each
for value, probability in zip(unique, prob):
    #print(f"Number {value} appeared with the probability {probability:.3f}")
    ...
    
#Visualize the probability

#Create bar graph with x=unique and y=probability
plt.bar(unique, prob)
#Title the graph as the following
plt.title("Probabilities of Dice rolls")
#Label the x axis as the following
plt.xlabel("Dice Roll")
#Label the y axis as the following
plt.ylabel("Probability")
#Create horizontal grid lines for easier readability
plt.grid(visible=True, axis='y')
#Show the graph
plt.show()