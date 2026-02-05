import sys


def main():
    print("Welcome to my Calculator!")
    while True:
        print("Choose selection below\n------------------")
        list_of_nums = []
        choice = input(
            "1. Addition\n2. Subtraction\n3. Multiplication\n4. Division\n5. Exit\n"
        )
        if choice == "1":
            try:
                nums = input("Enter numbers to add separated by a space: ").split(" ")
                for i in nums:
                    list_of_nums.append(int(i))
                print("Equals:", add(list_of_nums))
            except ValueError:
                print("Invalid input. Use numbers")
        elif choice == "2":
            try:
                nums = input("Enter numbers to subtract separated by a space: ").split(
                    " "
                )
                for i in nums:
                    list_of_nums.append(int(i))
                print("Equals:", subtract(list_of_nums))
            except ValueError:
                print("Invalid input. Use numbers")
        elif choice == "3":
            try:
                nums = input("Enter numbers to multiply separated by a space: ").split(
                    " "
                )
                for i in nums:
                    list_of_nums.append(int(i))
                print("Equals:", multiply(list_of_nums))
            except ValueError:
                print("Invalid input. Use numbers")
        elif choice == "4":
            try:
                nums = input("Enter 2 numbers to divide separated by a space: ").split(
                    " "
                )
                for i in nums:
                    list_of_nums.append(int(i))
                if len(list_of_nums) > 2:
                    print("Invalid input. Only use two numbers")
                    continue
                if list_of_nums[1] == 0:
                    print("Cannot Divide by zero")
                    continue
                print("Equals:", divide(list_of_nums))
            except ValueError:
                print("Invalid input. Use numbers")
        elif choice == "5":
            sys.exit("Thank you for using my Calculator!")
        else:
            print("Invalid input")


def add(nums_to_add):
    answer = 0
    for i in nums_to_add:
        answer += i
    return answer


def subtract(nums_to_sub):
    answer = nums_to_sub[0]
    for i in nums_to_sub[1:]:
        answer -= i
    return answer


def multiply(nums_to_mult):
    answer = nums_to_mult[0]
    for i in nums_to_mult[1:]:
        answer *= i
    return answer


def divide(nums_to_divide):
    return nums_to_divide[0] / nums_to_divide[1]


if __name__ == "__main__":
    main()
