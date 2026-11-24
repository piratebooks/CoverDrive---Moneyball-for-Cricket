import csv
import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from functions import OUTPUT_PATH_CLEANED, RAW_DATASET_PATH

bbb_base_path = RAW_DATASET_PATH / "Ball by ball"
output_players = OUTPUT_PATH_CLEANED

players_dict = {}

# Scan every Cricsheet *_info.csv file via rglob (recursive) for "info,registry,people" rows, which pair a player's
# name (row[3]) with their unique ID (row[4]) and store them in players_dict as {player_id: name}
# Deduplicates automatically since the Cricsheet ID is unique and dictionaries do NOT allow duplicates
# Tried to get it directly to a csv, but its RAM consuming and much slower 
for info_file in bbb_base_path.rglob("*_info.csv"):
    with open(info_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if (len(row) <= 5 and row[0] == "info" and
                row[1] == "registry" and
                row[2] == "people"):
                players_dict[row[4].strip()] = row[3].strip()


df_players = pd.DataFrame(
    list(players_dict.items()),
    columns=["Player_ID", "Cricsheet_Name"]
)
# Rudimentary data analysis
print(f"Total unique players extracted: {len(df_players)}")
print(df_players.head(10))
print(df_players.tail(10))
r_row = df_players.sample()
print(r_row)

# Making sure both are string values
df_players["Cricsheet_Name"] = df_players["Cricsheet_Name"].astype(str)
df_players["Player_ID"] = df_players["Player_ID"].astype(str)

# Sort by name
df_players.sort_values(by="Cricsheet_Name", inplace=True)
print("Ordered by Player Name, done :)")

#Getting some info for the last time
df_players.info()

# Output as players.csv
df_players.to_csv(output_players / "players.csv", index=False)

