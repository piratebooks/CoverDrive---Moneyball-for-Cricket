# Changelog

## Up until 2026-11-22 (Changelog generated via AI since I hadn't initalized git then):

### Ball-by-ball team analysis
- Scanned the BBL, IPL, and T20 Blast ball-by-ball folders.
- Used the `all_matches*.csv` files to identify and review team names across competitions.
- Checked for name discrepancies and teams that appeared only for a limited period.
- Specifically reviewed the Warwickshire/Birmingham Bears naming issue and the need to standardize team names before loading ball-by-ball data.

### Team normalization
- Added team-name normalization to the wider dataset design.
- Added mappings for rebranded or changed IPL franchises:
  - Kings XI Punjab -> Punjab Kings
  - Delhi Daredevils -> Delhi Capitals
  - Rising Pune Supergiants -> Rising Pune Supergiant
  - Royal Challengers Bangalore -> Royal Challengers Bengaluru
- Added team dimension records for IPL, BBL, and T20 Blast teams.
- Assigned each team to a league through `League_ID`.

## 19 November 2026

### Dataset troubleshooting
- Diagnosed an error in `datasets.py`.
- Applied the fix and rechecked the affected merge and cleaning stages.

## 20 November 2026

### Dataset script cleanup
- Removed dead code from `datasets.py`.
- Reduced unnecessary duplication and made the remaining merge and normalization flow easier to follow.

## 21 November 2026

### Removed player origin support
- Removed the `origin_id` CSV mapping and all origin-related processing from the project.
- Removed the `Player Origin` column from the auction merge.
- Removed the obsolete `player_origins.csv` deliverable.
- Simplified the auction data to the fields required for the planned database model.

## 22 November 2026

### Error fixes and code cleanup
- Fixed an indentation and execution-flow error in `player_table.py`.
- Identified and resolved the `pd` import issue by placing imports and code in valid scope.
- Reviewed `df_players.info()` and confirmed that the player DataFrame can be inspected successfully.
- Verified that `player_table.py` can extract player IDs and names from the ball-by-ball registry files.

# 2026-11-22

- Added more reusable paths in `functions.py`:
  - `BASE_PATH`
  - `OUTPUT_PATH_CLEANED`
  - `RAW_DATASET_PATH`
- Removed duplicate imports and unused variables while preserving existing comments and processing behavior.
- Removed the `League` column from the merged auction dataset

### Player extraction
- Created file `player_table.py` to build `Cleaned datasets/players.csv`
- Verified Output was consistent and truly deduplicated
- Removed some dead code relating to `league_info` to maintain 3NF

## 2026-11-23
- Used sys and subprocess to make sure `player_table.py` gets executed right after `datasets.py`

## 2026-11-24
 - Pushed to github and excluded *_info files from being tracked
 - Made the info files into 3 seperate zip files so its small and easy to track
 - Created the `README.md` file
 - Created the folder `Dataset_Functions`, such that future Streamlit and other folders will not get messed up
- Kept the shared path module at the repository root while grouping the dataset scripts in `Dataset_Functions`.

## Current file tree:

CoverDrive/
├── Dataset_Functions/
│   ├── datasets.py
│   └── player_table.py
├── Cleaned datasets/
├── Raw datasets/
├── functions.py
├── .gitignore
├── LICENSE
├── README.md
└── changelog.md