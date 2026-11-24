# CoverDrive: Moneyball for Cricket

CoverDrive is a player recommender system for the Indian Premier League (IPL), inspired by the *Moneyball* approach to scouting. Pick a star player and the system suggests a similar alternative batter for cheaper from one of three leagues: the Indian Premier League (IPL), the T20 Blast or the Big Bash League (BBL).

This is my individual project for my undergraduate module in UWE Bristol.

> **Status:** In progress. Expected completion: February.

## How It Works

A K-Nearest Neighbours (KNN) recommender does the heavy lifting. The user selects a star player and the model finds the most statistically similar batter using ball-by-ball data from [Cricsheet](https://cricsheet.org/), which is freely available and is the gold standard. Streamlit will be used to power the dashboard, likely hosted in Streamlit Community Cloud or Hugging Face spaces.

## Scope

**Covered**
- Batters only
- Recommendations from the IPL, T20 Blast and BBL

**Not covered**
- Injury data
- Win prediction
- Umpire-related data
- Auction price prediction

## Getting Started

1. Clone the repository.
2. Extract the zip files in the following folders before running anything:
   - `raw datasets\ball by ball\BBL`
   - `raw datasets\ball by ball\IPL`
   - `raw datasets\ball by ball\T20B`

   _Contains the info files for each of the matches present in `all_matches_xxx.csv`, where all the match metadata can be found in the info files_ 
3. Run `datasets.py`.

`datasets.py` and `player_table.py` are chained using `subprocess` and `sys` so running the first automatically triggers the second.

## Data Sources

- [Cricsheet ball-by-ball downloads](https://cricsheet.org/downloads/#experimental)
- [Cricsheet register](https://cricsheet.org/register/)
- [IPL Auction Dataset 2013-2026 (Kaggle)](https://www.kaggle.com/datasets/sunnyyadav754/ipl-auction-dataset-20132026)
