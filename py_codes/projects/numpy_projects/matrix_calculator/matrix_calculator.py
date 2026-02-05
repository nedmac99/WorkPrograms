import numpy as np
import sys

'''
Create a program that accepts 2D matricies and be able to perform the following:
-Addition
-Subtraction
-Element-wise multiplication
-Matrix multiplication
-Transposition(Flip over diagonal line)
'''
def main():
    print("Create array 1 \n")
    arr1 = create_array()
    print("\nCreate array 2: \n")
    arr2 = create_array()
    while True:
        choice = input("\nEnter choice of what to do to Matricies: \n1.Addition\n2.Subtraction\n3.Element-Wise Multiplication\n4.Dot Product\n5.Transpostion First Array\n6.Transposition Second array\n7.Exit\n")

        match (choice):
            case "1":
                print(f"\nSum: {sum_matrix(arr1, arr2)}\n")
            case "2":
                print(f"\nDifference: {diff_matrix(arr2, arr1)}\n")
            case "3":
                print(f"\nElement Mulitplication: {elem_mult(arr1, arr2)}\n")
            case "4":
                print(f"\nDot Product: {dot_product(arr1, arr2)}\n")
            case "5":
                print(f"\nTransposition of array 1: {transposed_arr1(arr1)}\n")
            case "6":
                print(f"\nTransposition of array 2: {transposed_arr2(arr2)}\n")
            case "7":
                sys.exit("Thanks for using my Matrix Calculator!")
            case _:
                print("Invalid Input")

def create_array():
    while True:
        try:
            a = int(input("Enter value for 1st: "))
            b = int(input("Enter value for 2nd: "))
            c = int(input("Enter value for 3rd: "))
            d = int(input("Enter value for 4th: "))
            break
        except ValueError:
            print("Not Numbers. Try again")
    return np.array([[a, b], [c, d]])

def sum_matrix(arr1, arr2):
    return arr1 + arr2

def diff_matrix(arr1, arr2):
    return arr1 - arr2

def elem_mult(arr1, arr2):
    return arr1 * arr2

def dot_product(arr1, arr2):
    return np.dot(arr1, arr2)

def transposed_arr1(arr1):
    return arr1.T

def transposed_arr2(arr2):
    return arr2.T

if __name__ == "__main__":
    main()