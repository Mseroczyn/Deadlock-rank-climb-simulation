# Deadlock-rank-climb-simulation
Monte Carlo simulation estimating the games needed to climb one full Deadlock rank at different win rates, with configurable loss-protection and win-streak assumptions.

Deadlock Rank-Climb Simulation
A small Monte Carlo simulation that estimates how many games are needed to climb one full rank in Deadlock at different win rates.
For example:
Start: Ritualist I with 0 Rank Points
Target: Emissary I
Total RP required: `5 × 1000 + 2000 = 7000 RP`
The script is intentionally simple and uses only Python's standard library.
What the simulation does
For each selected win rate, the script simulates many independent players.
Each simulated player:
Starts at Rank I with 0 RP.
Wins each game with the selected probability.
Gains RP for wins and loses RP for losses.
Moves through the six subranks.
Stops when they reach the next Rank I or the maximum game limit.
The script then reports:
how many simulated players reached the next rank;
the percentage that reached it;
the median number of games among successful climbs;
the mean number of games among successful climbs;
the 10th and 90th percentiles among successful climbs.
Modelled rules
The current script uses:
`+300 RP` for a normal win;
`-300 RP` for a loss;
five protected losses at a full-rank boundary;
two protected losses at other subrank boundaries;
a configurable win-streak bonus;
no additional loss-streak penalty.
A full-rank climb costs:
```text
Rank I -> II       1000 RP
Rank II -> III     1000 RP
Rank III -> IV     1000 RP
Rank IV -> V       1000 RP
Rank V -> VI       1000 RP
Rank VI -> next I  2000 RP
Total              7000 RP
```
Important assumptions

The simulation uses the following win-streak bonuses, based on the values shown in the in-game ranked tooltip:

1st consecutive win: +300 RP
2nd consecutive win: +300 RP
3rd consecutive win: +370 RP (+70 streak bonus)
4th consecutive win: +390 RP (+90 streak bonus)
5th consecutive win: +410 RP (+110 streak bonus)
6th consecutive win: +430 RP (+130 streak bonus)
7th and later wins:  +430 RP (+130 streak bonus)

The streak bonus is therefore capped at +130 RP from the sixth consecutive win onward.

This is controlled by:

USE_STREAK_BONUS = True

STREAK_BONUSES = {
    3: 70,
    4: 90,
    5: 110,
    6: 130,
}

Loss protection is modelled as follows:

protection is used only when a loss begins at exactly 0 RP;
Rank I boundaries receive five protected losses;
other subrank boundaries receive two;
protection refreshes when the player promotes into a subrank;
demotion does not grant protection.

These loss-protection details remain modelling choices where the exact behaviour of the live system is not completely known.

Settings
WIN_RATES = [46, 48, 50, 52, 55, 60]

SIMULATIONS = 10_000
MAX_GAMES = 10_000

BASE_POINTS = 300

USE_PROTECTION = True

USE_STREAK_BONUS = True
STREAK_BONUSES = {
    3: 70,
    4: 90,
    5: 110,
    6: 130,
}

SIMULATIONS is the number of independent simulated climbs for each win rate. MAX_GAMES is the maximum number of games allowed for each simulated player. A player stops earlier when they reach the target.
Example results
Using 10,000 simulations per win rate, a 10,000-game limit, loss protection, and the default streak assumptions:
Win rate	Reached next rank	Median games among successes	Mean games among successes	10th–90th percentile
46%	12.4%	275	386	94–791
48%	59.2%	541	1,206	133–3,179
50%	99.9%	396	717	117–1,693
52%	100.0%	224	304	88–618
55%	100.0%	134	160	66–289
60%	100.0%	84	92	47–147
The mean and median are conditional on reaching the target before `MAX_GAMES`. This matters especially when the completion percentage is low.
For example, at 46%, the median of 275 games describes only the 12.4% of simulations that succeeded. It does not mean a typical 46% player ranks up in 275 games.
Interpreting the 50% result
Without streak bonuses or protection, a 50% win rate has zero expected RP drift.
In this model, win streaks increase the reward for wins while loss streaks do not increase the loss penalty. Loss protection also prevents some RP loss. Together, these assumptions create upward pressure even at a 50% win rate.
The 50% result should therefore be understood as a result of this particular model, not proof of the exact live Deadlock system.
Simple mathematical benchmark
Ignoring streak bonuses, protection, matchmaking adjustments, and randomness:
```text
Expected RP per game =
(win rate × 300) + (loss rate × -300)
```
At 52%:
```text
(0.52 × 300) + (0.48 × -300) = 12 RP per game
```
The simple drift estimate is:
```text
7000 / 12 = approximately 583 games
```
This is an average-drift benchmark, not a prediction that every player will take exactly 583 games.
Limitations
The simulation does not model:
any additional or hidden modifiers to the published win-streak bonuses;
matchmaking-based RP adjustments;
larger penalties during loss streaks;
changing win probability as the player climbs or falls;
hidden MMR;
season resets;
abandons or voided games;
dynamic Eternus thresholds.
The project is best used for comparing explicit assumptions rather than reproducing the live ranking system exactly.
Background
This project was inspired by the following discussion:
https://www.reddit.com/r/DeadlockTheGame/comments/1vcrsyn/you_will_climb_in_deadlock_ranked_with_a_452/
