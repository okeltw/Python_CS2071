"""The Game of Hog."""

"""
Taylor Okel
Python Programming
Homework 1

This file is a conglomerate of hog.py and hog_extra.py as provided.
    Additionally, the "hog_eval" file was not provided (when I first downloaded,
    sometime around 2/1/17 -- it may have been included after?), so I wrote a
    final strategy eval function that averages the win rate over a number of
    samples (default 100). Use '-f' or '--final' to access this.
"""

from dice import four_sided, six_sided, make_test_dice


GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """
    >>> roll_dice(1,make_test_dice(4, 2, 1, 3))
    4
    >>> roll_dice(2,make_test_dice(4, 2, 1, 3))
    6
    >>> roll_dice(3,make_test_dice(4, 2, 1, 3))
    1
    >>> roll_dice(4,make_test_dice(4, 2, 1, 3))
    1
    """

    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN Question 1
    total = 0
    for i in range(num_rolls):
        roll = dice()

        if roll == 1:
            return 1
        else:
            total += roll

    return total
    # END Question 1


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """
    >>> take_turn(2, 0, make_test_dice(4, 6, 1))
    10
    >>> take_turn(3, 0, make_test_dice(4, 6, 1))
    1
    >>> take_turn(0, 35)
    6
    >>> take_turn(0, 71)
    8
    >>> take_turn(0, 7)
    8
    >>> take_turn(0, 0)
    1
    >>> take_turn(0, 9)
    10
    >>> take_turn(2, 0, make_test_dice(6))
    12
    >>> take_turn(0, 50)
    6
    """
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN Question 2
    if num_rolls == 0:
        return free_bacon(opponent_score)

    return roll_dice(num_rolls, dice)
    # END Question 2

def free_bacon(opponent_score):
    digits = [int(i) for i in str(opponent_score)]
    return max(digits)+1

def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).

    >>> select_dice(4, 24) == four_sided
    True
    >>> select_dice(16, 64) == four_sided
    False
    >>> select_dice(0, 0) == four_sided
    True
    >>> select_dice(50, 80) == four_sided
    False
    """
    # BEGIN Question 3
    if (score + opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided
    # END Question 3

def is_swap(score0, score1):
    """Return True if ending a turn with SCORE0 and SCORE1 will result in a
    swap.

    Swaps occur when the last two digits of the first score are the reverse
    of the last two digits of the second score.

    >>> is_swap(19, 91)
    True
    >>> is_swap(20, 40)
    False
    >>> is_swap(41, 14)
    True
    >>> is_swap(23, 42)
    False
    >>> is_swap(55, 55)
    True
    >>> is_swap(114, 41) # We check the last two digits
    True
    """
    # BEGIN Question 4
    dig0 = [int(i) for i in str(score0)]
    dig1 = [int(j) for j in str(score1)]

    x = len(dig0)
    y = len(dig1)

    return ((dig0[x-1] == dig1[y-2]) and (dig0[x-2] == dig1[y-1]))
    # END Question 4

# i just used an xor
def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN Question 5
    while score0 < goal and score1 < goal:
        dice = select_dice(score0, score1)

        if not who: # if player 0
            score0 += take_turn(strategy0(score0, score1), score1, dice)
        else:
            score1 += take_turn(strategy1(score1, score0), score0, dice)

        if is_swap(score0, score1):
            score0, score1 = score1, score0

        who = who^1 #who XOR 1 => bit flip
    # END Question 5
    return score0, score1


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

### Extra Credit ###

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    # BEGIN Question 6
    def helper(*args):
        total = 0
        for it in range(num_samples):
            total += fn(*args)

        return total / 1000

    return helper
    # END Question 6


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7
    average = make_averaged(roll_dice, num_samples)
    results = [0] * 10
    for it in range(10):
        results[it] = average(it+1, dice)

    return results.index(max(results))+1
    # END Question 7


## Extra Credit ##

##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.


def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--final', '-f', action='store_true',
                        help='Display the final_strategy win rate against always_roll(5)')
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
    elif args.final:
        #from hog_eval import final_win_rate
        win_rate = final_win_rate()
        print('Your final_strategy win rate is')
        print('    ', win_rate)
        print('(or {}%)'.format(round(win_rate * 100, 2)))

#######################
# Phase 2: Strategies #
#######################

from hog import *
from dice import *

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6ma, scoring 11.
    Thus, the average value is 6.0.
    """
    # BEGIN Question 6
    def helper(*args):
        total = 0
        for it in range(num_samples):
            total += fn(*args)

        return total / 1000

    return helper
    # END Question 6

def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7
    average = make_averaged(roll_dice, num_samples)
    results = [0] * 10
    for it in range(10):
        results[it] = average(it+1, dice)

    return results.index(max(results))+1
    # END Question 7

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    score = 0 #random.randint(0,100)
    opponent_score = 0 #randint(0,100)

    if True: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if True: # Change to True to test always_roll(8)
        print('always_roll(5) win rate:', average_win_rate(always_roll(5)))

    if True: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy(score, opponent_score)))

    if True: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy(score, opponent_score)))

    if True:
        wr = average_win_rate(final_strategy(score, opponent_score))

        print('final_strategy win rate:', wr)

    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 8
    def strategy(score, opponent_score):
        if free_bacon(opponent_score) >= margin:
            return 0
        else:
            return num_rolls

    return strategy
    # END Question 8

def swap_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial swap and
    rolls NUM_ROLLS if rolling 0 dice results in a harmful swap. It also
    rolls 0 dice if that gives at least MARGIN points and rolls NUM_ROLLS
    otherwise.
    """
    # BEGIN Question 9
    def strategy(score, opponent_score):
        post_bacon = score + free_bacon(opponent_score)
        if opponent_score > post_bacon and is_swap(post_bacon, opponent_score):
            return 0
        else:
            return bacon_strategy(score, opponent_score, margin, num_rolls)(score, opponent_score)

    return strategy
    # END Question 9


def final_strategy(score, opponent_score):
    """
    If free bacon will result in a win (without swapping), take this route.

    Use a number of rolls based on the maximum value (experimentally) of dice
    rolls for the dice I'm stuck with.

    Adjust the number of rolls for large leads:
        If ahead, play conservatively
        If behind, time to take risks

    Then, if I am winning:
        always roll dice if free bacon will result in a swap.
        use free bacon if it will force opponent to use four-sided
        use the free bacon strategy with a margin of 8 for everything else.
    Otherwise, if I am losing:
        always use free bacon if it will swap or force four-sided.
        use the free bacon strategy as if winning for everything else.

    This has been imperically shown to get around a 59% win rate.
    Further improvements could be found by experimenting with the "magic
        numbers", or the effectiveness of using the bacon strategy instead of
        pure rolls in various situations.
    """
    # BEGIN Question 10
    def strategy(score, opponent_score):
        losing =        score <= opponent_score
        post_bacon =    score + free_bacon(opponent_score)
        dice =          select_dice(score, opponent_score)
        will_be_four =  select_dice(post_bacon, opponent_score) == four_sided
        swap =          is_swap(post_bacon, opponent_score)

        if post_bacon >= 100 and not swap:
            return 0


        if dice == four_sided:
            num_rolls = 4
        elif dice == six_sided:
            num_rolls =  6

        if not losing and score - opponent_score > 15:
            num_rolls -= 2
        elif losing and opponent_score - score > 15:
            num_rolls += 1

        if not losing:
            if swap:
                return num_rolls
            elif will_be_four:
                return 0
            else:
                return  bacon_strategy(score, opponent_score, 8, num_rolls)(score, opponent_score)
        else:
            if (swap and not post_bacon > opponent_score) or will_be_four:
                return 0
            else:
                return bacon_strategy(score, opponent_score, 8, num_rolls)(score, opponent_score)


    return strategy
    # END Question 10

    # END Question 10

def final_win_rate(num_samples=100):
    wr = 0
    for x in range(0,num_samples):
        wr += average_win_rate(final_strategy(0,0))

    return wr / x

if __name__=="__main__": run()
