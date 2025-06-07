"""
Wordle game
Guess the 5-letter word in 6 tries
"""
import random

def main():
    wordlist = load_words_from_file("wordlist.txt")

    print("Welcome to Wordle!")
    print("Rule: You must guess the word in 6 tries.")
    print("The word changes every day.")

    word_of_the_day = random.choice(wordlist)
    #print(f"Word of the day is {word_of_the_day}!")  # Only for testing purposes

    for attempt in range(6):
        input_word = input("Enter your guess: ").strip().lower()
        
        if len(input_word) != len(word_of_the_day):
            print("Please enter a 5-letter word.")
            continue  # Skip this attempt if word length is incorrect

        feedback = ""
        for i in range(len(word_of_the_day)):
            if input_word[i] == word_of_the_day[i]:
                feedback += input_word[i].upper()  # Correct letter and position
            elif input_word[i] in word_of_the_day:
                feedback += input_word[i]  # Correct letter but wrong position
            else:
                feedback += "-"  # Letter not in the word
        print(f"Feedback: {feedback}")

        if input_word == word_of_the_day:
            print("Congratulations! You guessed the word!")
            break
    else:
        print(f"Sorry, you used all attempts. The word was: {word_of_the_day}")




def load_words_from_file(filepath):
    wordlist = []
    with open(filepath, 'r') as file_reader:
        for line in file_reader.readlines():
            cleaned_line = line.strip()
            if cleaned_line != '':
                wordlist.append(cleaned_line)
    
    return wordlist

if __name__ == "__main__":
    main()
