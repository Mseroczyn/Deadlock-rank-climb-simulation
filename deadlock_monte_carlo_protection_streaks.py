"""
Simple Deadlock Monte Carlo simulation.

Question:
Starting at Rank I with 0 RP, how many games does it take
to reach the next Rank I at a given win rate?

Run:
Open this file in PyCharm, edit the settings below,
then right-click -> Run.
"""

import random
import statistics


# -------------------- SETTINGS --------------------

WIN_RATES = [46, 48, 50, 52, 55, 60]

SIMULATIONS = 10_000
MAX_GAMES = 10_000

BASE_POINTS = 300

# Loss protection
USE_PROTECTION = True

# Win-streak bonus assumptions
#
# Example with the settings below:
# 1st win: +300
# 2nd win: +300
# 3rd win: +330
# 4th win: +360
# 5th win: +390
# ...
# Maximum win value: +450
USE_STREAK_BONUS = True
STREAK_START = 3
STREAK_STEP = 30
MAX_STREAK_BONUS = 150

# Promotion costs:
# I -> II, II -> III, III -> IV, IV -> V, V -> VI, VI -> next Rank I
COSTS = [1000, 1000, 1000, 1000, 1000, 2000]


# -------------------- HELPER FUNCTIONS --------------------

def promotion_cost(state):
    """
    Return the RP needed to leave the current subrank.

    state = 0 means starting Rank I
    state = 1 means starting Rank II
    ...
    state = 5 means starting Rank VI
    state = 6 means next Rank I

    Negative states represent ranks below the starting rank.
    """
    return COSTS[state % 6]


def protection_at(state):
    """
    Rank I boundaries get 5 protected losses.
    Other subrank boundaries get 2.
    """
    if not USE_PROTECTION:
        return 0

    if state % 6 == 0:
        return 5

    return 2


def points_for_win(win_streak):
    """
    Return the RP gained for a win.

    The exact Deadlock streak formula is unknown.
    These settings are only an assumption for testing.
    """
    if not USE_STREAK_BONUS:
        return BASE_POINTS

    bonus_steps = max(0, win_streak - STREAK_START + 1)
    bonus = min(bonus_steps * STREAK_STEP, MAX_STREAK_BONUS)

    return BASE_POINTS + bonus


def percentile(values, percent):
    """Return a simple percentile from a sorted list."""
    values = sorted(values)
    index = round((len(values) - 1) * percent)
    return values[index]


# -------------------- ONE SIMULATED CLIMB --------------------

def simulate_one_climb(win_rate):
    """
    Simulate one player until they reach the next full rank.

    Returns:
        Number of games required.

    Returns None if:
        The player does not reach the next rank before MAX_GAMES.
    """
    state = 0
    rp = 0

    protection = protection_at(state)
    win_streak = 0

    for game in range(1, MAX_GAMES + 1):

        won = random.random() < win_rate

        if won:
            win_streak += 1
            rp += points_for_win(win_streak)

            # Promote while the player has enough RP.
            while rp >= promotion_cost(state):
                rp -= promotion_cost(state)
                state += 1

                # Protection refreshes whenever the player promotes
                # into a new subrank.
                protection = protection_at(state)

                # Six promotions means the next full rank was reached.
                if state == 6:
                    return game

        else:
            win_streak = 0

            # Protection is used only if the player started the game
            # exactly at a 0 RP boundary.
            started_at_zero = rp == 0

            rp -= BASE_POINTS

            if rp < 0:
                if started_at_zero and protection > 0:
                    protection -= 1
                    rp = 0
                else:
                    # Demote one subrank and carry the remaining RP loss.
                    state -= 1
                    rp += promotion_cost(state)

                    # Protection is not granted after a demotion.
                    protection = 0

    return None


# -------------------- RUN THE SIMULATION --------------------

random.seed(1)

for win_rate_percent in WIN_RATES:
    win_rate = win_rate_percent / 100

    results = []

    for _ in range(SIMULATIONS):
        games = simulate_one_climb(win_rate)

        if games is not None:
            results.append(games)

    completion_rate = len(results) / SIMULATIONS * 100

    print()
    print("Win rate:", str(win_rate_percent) + "%")
    print("Successful climbs:", len(results), "out of", SIMULATIONS)
    print("Reached next rank:", f"{completion_rate:.1f}%")

    if results:
        print(
            "Median games among successful climbs:",
            round(statistics.median(results))
        )
        print(
            "Mean games among successful climbs:",
            round(statistics.mean(results))
        )
        print(
            "10th percentile among successful climbs:",
            percentile(results, 0.10)
        )
        print(
            "90th percentile among successful climbs:",
            percentile(results, 0.90)
        )
    else:
        print("Nobody reached the next rank before MAX_GAMES.")
