class Account:
    def __init__(self):
        self._balance = 0
    
    @property
    def balance(self):
        return f"Balance is: {self._balance}"

    def deposit(self, n):
        self._balance += n

    def withdraw(self, n):
        self._balance -= n
        
def main():
    account = Account()
    print(account.balance)
    account.deposit(100)
    account.withdraw(50)
    print(account.balance)

if __name__ == "__main__":
    main()



'''
balance = 0

#Without specifying that it is a Global variable it will throw an UnboundLocalError. Add global before the use of the variable to prevent this

def main():
    print("Balance: ", balance)
    deposit(100)
    withdraw(50)
    print("Balance: ", balance)
    
def deposit(n):
    global balance
    balance += n
    
def withdraw(n):
    global balance
    balance -= n
    
        
if __name__ == "__main__":
    main()

'''