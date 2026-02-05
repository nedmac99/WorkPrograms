import sys
import csv
import random

easy_words_list = []
medium_words_list = []
hard_words_list = []
scholar_words_list = []

def main():

    print("Welcome to my hangman game!\n---------------------------")
    difficulty = input("Enter difficulty: \n1. Easy\n2. Medium\n3. Hard\n4. Scholar\n")
    
    if difficulty == "1":
        secret_word = read_file_easy()
    elif difficulty == "2":
        secret_word = read_file_medium()
    elif difficulty == "3":
        secret_word = read_file_hard()
    elif difficulty == "4":
        secret_word = read_file_scholar()
    else:
        sys.exit("Invalid choice")
    
    word_as_list = []
    for i in secret_word:
        word_as_list.append(i)
    attempts = 6
    length = len(secret_word)
    used_letters = []
    placeholder = ["_" for _ in secret_word]
    while attempts > 0:
        print(f"There are {length} letters left to guess in the word\n")
        print(placeholder,"\n")
        guess = input(f"Guess letter or word(Attempts left {attempts}): \n").lower().strip()

        if guess == secret_word:
            print(f"{guess} is correct!")
            break
        
        elif guess in used_letters:
            print("Already guessed that letter\n")
            continue
        
        elif guess in word_as_list:
            count = 0
            for index, letter in enumerate(secret_word):
                if letter == guess:
                    placeholder[index] = guess
                    count += 1
            print(f"{guess} is in the word {count} times\n")
            used_letters.append(guess)
            length -= count
            
        else:
            print("Incorrect guess\n")
            attempts -= 1
            
    if attempts == 0:    
        print(f"You Lose! The word was {secret_word}")
              
        
def read_file_easy():
    with open("C:\\Users\\Dwhite\\py_codes\\projects\\hangman\\words_for_hangman.csv", "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            easy_words = line["easy"]
            easy_words_list.append(easy_words)
        easy_rand = random.choice(easy_words_list)
        return easy_rand
    
def read_file_medium():
    with open("C:\\Users\\Dwhite\\py_codes\\projects\\hangman\\words_for_hangman.csv", "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            medium_words = line["medium"]
            medium_words_list.append(medium_words)
        medium_rand = random.choice(medium_words_list)
        return medium_rand
    
def read_file_hard():
    with open("C:\\Users\\Dwhite\\py_codes\\projects\\hangman\\words_for_hangman.csv", "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            hard_words = line["hard"]
            hard_words_list.append(hard_words)
        hard_rand = random.choice(hard_words_list)
        return hard_rand
    
def read_file_scholar():
    with open("C:\\Users\\Dwhite\\py_codes\\projects\\hangman\\words_for_hangman.csv", "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            scholar_words = line["scholar"]
            scholar_words_list.append(scholar_words)
        scholar_rand = random.choice(scholar_words_list)
        return scholar_rand
    
    
if __name__ == "__main__":
    main()
    
#Print entire list#
#for words in easy_words_list:
        #print(f"{words["easy"]}")
