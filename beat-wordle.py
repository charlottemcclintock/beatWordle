'''
Charlotte + Rohit 
fun saturday code around puzzle
'''

'''
STEP ONE: guess a first word, with some vowels. 
random word with at least three different vowels.
'''
import random
import regex as re
import pandas as pd

# get list of 5 letter words
with open("dictionary.txt", 'r') as fh:
    fiveletterwords = [x[:5].upper() for x in fh.readlines()]

start_words = [word for word in fiveletterwords if len(set(list(word))) == len(word)]

def resultsFormattedCorrectly(results):
    valid = set(['*', '_', '?'])
    set_results = set(results)
    return set_results.issubset(valid) and len(results) == 5


def getFirstWord(): 
    first_word = random.choice(start_words) # when we're in the mood for some real fun again
    print(f'Your first word is {first_word}.')
    return first_word

current_guess =  list(getFirstWord())

'''
STEP TWO: record information gathered from step results. 
'''

results_format = '''
**input guide:**
_ letter is not in word. 
? letter is not in right spot. 
* letter is correct. 

ex. word is 'LIONS' results are '**_?_' if true word is 'LINUX'.
'''

# set up
round = 1
word_information = ['\w', '\w', '\w', '\w', '\w']
not_in_word = []
unknown_position = []
possible_words = fiveletterwords
wrong_position = []
guess_list = ''.join(current_guess)
n_words_left = [0, 0, 0, 0, 0, 0]
columns = ['round1', 'round2', 'round3', 'round4', 'round5', 'round6', 'guesses']

while True:

    n_words_left[round-1] = len(possible_words)

    results = list(input(f'What were the results round {round}?\n'))

    while not resultsFormattedCorrectly(results):
        print("Whoops! There is an input error, please re-type your results")
        results = list(input(f'What were the results round {round}?\n'))
    
    if results == list('*****'): 
        # write out game results
        n_words_left.append([guess_list])
        game_results = {columns[i]: n_words_left[i] for i in range(len(columns))}
        game_tracker = pd.read_csv('game-tracker.csv')
        game_tracker = game_tracker.append(pd.DataFrame(game_results), ignore_index=True)
        game_tracker.to_csv('game-tracker.csv', index=False)

        # celebrate!
        print(f'Woohoo! Congrats. You smashed it. You guessed the right answer in {round} tries.')
        break

    info = list(zip(list(range(0,5)),current_guess, results))

    for index, letter, symbol in info: 
        if symbol == '*': 
            word_information[index] = letter
        if symbol == '_': 
            not_in_word.append(letter)
        if symbol == '?':
            unknown_position.append(letter)
            wrong_position_regex = ['\w', '\w', '\w', '\w', '\w']
            wrong_position_regex[index] = letter
            wrong_position.append(''.join(wrong_position_regex))
    
    '''
    STEP THREE: 
    determine words that are still viable based on information. 
    '''

    # find words in list that are still possible based on current information
    round_words = []
    for test_word in possible_words: 
        # step one: does the word match the known pattern?
        word_regex = "".join(word_information)
        if re.search(word_regex, test_word) is None: 
            continue
        # step two: does the word contain the unknown position letters? 
        # does the word not contain the letter in the wrong place?
        unknown_count = 0
        bad_position_flag = False
        for letter in unknown_position: 
            if letter in test_word: 
                unknown_count += 1 
        for regex_match in wrong_position:
            if re.search(regex_match, test_word): 
                bad_position_flag = True
        if unknown_count != len(unknown_position) or bad_position_flag: 
            continue
        
        # step three: does the word not contain the known incorrect letters?
        death_letter = False
        for letter in not_in_word: 
            if letter in test_word and letter not in word_information and letter not in unknown_position: 
                death_letter = True
                break
        if death_letter:
            continue

        round_words.append(test_word)

    possible_words = round_words
    
    '''
    STEP FOUR: 
    make guess with random word that has tied highest likelihood. 
    and go back to step two. 
    '''

    next_guess = random.choice(possible_words)
    print(f'There are {len(possible_words)} possible words left for your game. Why not try {next_guess}?')
    if len(possible_words) <= 20:
        print(f'The possible words left are: {possible_words}')

    didUseGuess = input(f"Did you use {next_guess}? (y/n) ")
    if didUseGuess == "y" or didUseGuess == '':
        possible_words.remove(next_guess)
        current_guess = next_guess
    else:
        current_guess = input("How creative! What was your guess? ").upper()
        try: 
            possible_words.remove(current_guess)
        except: 
            pass


    # increment round counter
    round += 1
    guess_list =  guess_list + ' - ' + current_guess
    


"""
TODO
- fix data collection so it writes at end of game, not just at win
- automate data collection. 
- write to database instead of csv. 
- convert to terminal app
"""