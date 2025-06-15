from datetime import datetime, timezone
import random
import os

LOG_FILE = "game_log.txt"
WORD_FILE = "wordlist.txt"

def main():
    wordlist = load_words_from_file(WORD_FILE)
    time_utc = datetime.now(timezone.utc)
    current_date = time_utc.date().isoformat()

    if has_already_played(current_date):
        print("You've already played Wordle today. Come back tomorrow!")
        return

    word_of_the_day = random.choice(wordlist)
    # print(f"[DEBUG] Word of the day: {word_of_the_day}")

    print("Welcome to Wordle!")
    print("Rule: You must guess the word in 6 tries.")
    print("The word changes every day.")

    for attempt in range(1, 7):
        input_word = input("Enter your guess: ").strip().lower()

        if len(input_word) != len(word_of_the_day):
            print("Please enter a 5-letter word.")
            continue

        # Verify that the word is in the word list
        if input_word not in wordlist:
            print("That's not a valid word, try again.")
            continue

        feedback = ""
        for i in range(len(word_of_the_day)):
            if input_word[i] == word_of_the_day[i]:
                feedback += input_word[i].upper()
            elif input_word[i] in word_of_the_day:
                feedback += input_word[i]
            else:
                feedback += "-"

        print(f"Feedback: {feedback}")

        if input_word == word_of_the_day:
            print("Congratulations! You guessed the word!")
            save_game_log(current_date, attempt, True)
            return

    print(f"Sorry, you used all attempts. The word was: {word_of_the_day}")
    save_game_log(current_date, 6, False)

    display_stats(log_path="game_log.txt")


def load_words_from_file(filepath):
    with open(filepath, 'r') as file_reader:
        return [line.strip() for line in file_reader if line.strip() != '']


def has_already_played(date_str):
    if not os.path.exists(LOG_FILE):
        return False
    with open(LOG_FILE, 'r') as log:
        return any(line.startswith(date_str) for line in log)


def save_game_log(date_str, attempts, success):
    with open(LOG_FILE, 'a') as log:
        status = "Success" if success else "Failed"
        log.write(f"{date_str} - {status} in {attempts} attempts\n")

def display_stats(log_path="game_log.txt"):
    if not os.path.exists(log_path):
        print("No log data available.")
        return

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    if not lines:
        print("No game history yet.")
        return

    total_games = len(lines)
    total_wins = 0
    total_tries = 0
    win_days = 0
    dates = []

    for line in lines:
        date_str, rest = line.split(" - ")
        dates.append(datetime.strptime(date_str, "%Y-%m-%d").date())

        if "Success" in rest:
            total_wins += 1
            tries = int(rest.split("in ")[1].split(" ")[0])
            total_tries += tries
            win_days += 1

    average_tries = total_tries / win_days if win_days > 0 else None

    # Sort and calculate streaks
    dates.sort()
    max_streak = 0
    current_streak = 1
    for i in range(1, len(dates)):
        if dates[i] == dates[i-1] + timedelta(days=1):
            current_streak += 1
        else:
            max_streak = max(max_streak, current_streak)
            current_streak = 1
    max_streak = max(max_streak, current_streak)

    today = datetime.now(timezone.utc).date()
    last_played = dates[-1]
    is_today = last_played == today
    if is_today and len(dates) >= 2 and dates[-2] == today - timedelta(days=1):
        current_streak_display = current_streak
    elif is_today:
        current_streak_display = 1
    else:
        current_streak_display = 0

    # Display results
    print("\n📊 Game Statistics:")
    print(f"Total games played: {total_games}")
    print(f"Total wins: {total_wins}")
    print(f"Win rate: {100 * total_wins / total_games:.1f}%")
    print(f"Average tries (only successful games): {average_tries:.2f}" if average_tries else "Average tries: N/A")
    print(f"Max streak: {max_streak} day(s)")
    print(f"Current streak: {current_streak_display} day(s)")


if __name__ == "__main__":
    main()
