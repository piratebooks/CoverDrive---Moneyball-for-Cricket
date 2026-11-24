#THIS FILE WILL: 
# 1. Merge the auction Datasets after cleaning
# 2. Create dimension tables for franchises, leagues, currency, teams and player roles
# Make my life easier
# 3. Use some AI to identify player name inconsistencies and normalise them 
# 4. Output the cleaned datasets to cleaned datasets folder#
# Used AI to comment some pieces of code and refactor the long code lines. I'll fight u if you say it makes me a bad programmer
# This will also import subprocess and sys files to execute player extraction as soon as the first part of datasets is done
import sys
import time, subprocess
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from functions import OUTPUT_PATH_CLEANED, RAW_DATASET_PATH
main = RAW_DATASET_PATH / "Player pricing" / "IPLPlayerAuctionData.csv"
to_merge_2023 = RAW_DATASET_PATH / "Player pricing" / "IPL_Auction_2023_Sold_Player.csv"
to_merge_2024 = RAW_DATASET_PATH / "Player pricing" / "IPL_Auction_2024_Sold_Player.csv"

# teams for IPL to be created as a dimension table
teams_data = {
    "Team": [
        #IPL teams
        "Chennai Super Kings",
        "Delhi Capitals",
        "Gujarat Lions",
        "Gujarat Titans",
        "Kolkata Knight Riders",
        "Lucknow Super Giants",
        "Mumbai Indians",
        "Pune Warriors India",
        "Punjab Kings",
        "Rajasthan Royals",
        "Rising Pune Supergiant",
        "Royal Challengers Bengaluru",
        "Sunrisers Hyderabad",
        # BBL Teams
        "Adelaide Strikers",
        "Brisbane Heat",
        "Hobart Hurricanes",
        "Melbourne Renegades",
        "Melbourne Stars",
        "Perth Scorchers",
        "Sydney Sixers",
        "Sydney Thunder",
        # T20 Blast Teams
        "Derbyshire Falcons",
        "Durham",
        "Essex",
        "Glamorgan",
        "Gloucestershire",
        "Hampshire Hawks",
        "Kent Spitfires",
        "Lancashire Lightning",
        "Leicestershire Foxes",
        "Middlesex",
        "Northamptonshire Steelbacks",
        "Notts Outlaws",
        "Somerset",
        "Surrey",
        "Sussex Sharks",
        "Warwickshire Bears",
        "Worcestershire Rapids",
        "Yorkshire",
        ],
    "League_ID": [1] * 13 + [2] * 8 + [3] * 18 #Basically, for the first 13 or so rows, put 1, 
    # follow up by 8 number 2's, and then 18 number 3
    }


#same here
league_data = {
    'L_Name': [
        'Indian Premier League',
        'Big Bash League',
        'Vitality T20 Blast'],
    'L_Short': ['IPL', 'BBL', 'The Blast'],
    'Country': ['India', 'Australia', 'England and Wales'],
    'Governing_Body': ['BCCI', 'Cricket Australia', 'ECB'],
    'Year_Origin': [2008, 2011, 2003],
    'Currency_ID': [1, 2, 3],
    'Max_Overseas': [8, 7, 4]
}

player_role = {
    "Role": [
        "Batsman",
        "Bowler",
        "All-Rounder",
        "Wicketkeeper",
        "Wicketkeeper-Batsman",
        "Batting All-Rounder",
        "Bowling All-Rounder"
    ]
}

sold_in_currency = {
    'Currency_code': ['INR', 'AUD', 'GBP'],
    'Currency_name': ['Indian Rupee', 'Australian Dollar', 'British Pound']
}

# Load the main auction history + 2023/2024 records to merge with it
df_main = pd.read_csv(main)
df_2023 = pd.read_csv(to_merge_2023)
df_2024 = pd.read_csv(to_merge_2024)

print("df_main original shape:", df_main.shape)
print("df_2023 original shape:", df_2023.shape)
print("df_2024 original shape:", df_2024.shape)
print("-" * 60)

# Clean rows - Drop Nulls
df_main_cleaned = df_main.dropna(
    subset=["Player"]
).copy()  # so that the original df_main is not modified
df_2023_cleaned = df_2023.dropna(subset=["Player"]).copy()
df_2024_cleaned = df_2024.dropna(subset=["Player"]).copy()
print("Null values dropped. Current shapes after dropping nulls:")
print("df_main_cleaned shape:", df_main_cleaned.shape)
print("df_2023_cleaned shape:", df_2023_cleaned.shape)
print("df_2024_cleaned shape:", df_2024_cleaned.shape)

print("The primary dataset after cleaning:\n")
df_main_cleaned.info()
print("The 2023 supplementary dataset after cleaning:\n")
df_2023_cleaned.info()
print("The 2024 supplementary dataset after cleaning:\n")
df_2024_cleaned.info()

# Use string formating to remove commas and whitespace, then convert to numeric type
for df in [df_2023_cleaned, df_2024_cleaned]:
    df["Amount"] = df["Amount"].str.replace(",", "").str.strip()
    df["Amount"] = pd.to_numeric(df["Amount"]).astype("int64")
    print("Data type of Amount column after conversion:", df["Amount"].dtype)

# identify string columns in both datasets to normalize whitespace
for df in [df_main_cleaned, df_2023_cleaned, df_2024_cleaned]:
    string_cols = df.select_dtypes(include=["string", "object"]).columns

    # Normalize surrounding whitespace before combining the datasets.
    for col in string_cols:
        df[col] = (
            df[col].str.split().str.join(" ")
        )  # removes any trailing, following or double whitespace in between words
        # and replaces it with a single space.
        # This is important for matching player names and team names across datasets

# Make null values NaN, then make it 0, and finally convert the Year column to int64 type for both datasets
# Tried to make the code 'df_main_cleaned["Year"].fillna(0).astype(int64)', but it just kept breaking for some reason
df_main_cleaned["Year"] = (
    pd.to_numeric(df_main_cleaned["Year"], errors="coerce").fillna(0).astype("int64")
)
df_2023_cleaned["Year"] = (
    pd.to_numeric(df_2023_cleaned["Year"], errors="coerce").fillna(0).astype("int64")
)
df_2024_cleaned["Year"] = (
    pd.to_numeric(df_2024_cleaned["Year"], errors="coerce").fillna(0).astype("int64")
)
# ishan porel issue = only bugger with year 0
df_main_cleaned.loc[
    (df_main_cleaned["Player"] == "Ishan Porel") & (df_main_cleaned["Year"] == 0),
    "Year",
] = 2019

# Merge the datasets
merge_auction = pd.concat(
    [df_main_cleaned, df_2023_cleaned, df_2024_cleaned], ignore_index=True
)

# Used AI to identifiy player inconsistencies, manually mapped them
player_name_map = {
    "Akila Dananjaya": "Akila Dhananjaya",
    "Akshar Rajesh Patel": "Axar Rajesh Patel",
    "Barinder Singh Saran": "Barinder Singh Sran",
    "Bhagath Varma": "K.Bhagath Varma",
    "C Hari Nishaanth": "C.Hari Nishaanth",
    "Dan Christian": "Daniel Christian",
    "Dushmanta Chameera": "Dushmantha Chameera",
    "K.C Cariappa": "K.C. Cariappa",
    "M. Ashwin": "Murugan Ashwin",
    "N Jagadeesan": "N. Jagadeesan",
    "Mujeeb Rahman": "Mujeeb Zadran",
    "M Siddharth": "M. Siddharth",
    "Nicolas Pooran": "Nicholas Pooran",
    "Praveen Dubey": "Pravin Dubey",
    "R. Sanjay Yadav": "Sanjay Yadav",
    "Rahul Ajay Tripathi": "Rahul Tripathi",
    "Sarfaraz Naushad Khan": "Sarfaraz Khan",
    "Siddarth Kaul": "Siddharth Kaul",
    "Suyash Prabhudesai": "Suyash Prabhudessai",
    "T Natarajan": "T. Natarajan",
    "Tejas Baroka": "Tejas Singh Baroka",
    "Yuzvendra Singh Chahal": "Yuzvendra Chahal",
    "Ankit Nagendra Sharma": "Ankit Sharma",
    "Mandeep Hardev Singh": "Mandeep Singh",
}
merge_auction["Player"] = merge_auction["Player"].replace(
    player_name_map
)
# Role inconsistencies changing
merge_auction["Role"] = merge_auction["Role"].replace(
    {
        "Wicket Keeper": "Wicketkeeper",
        "Wicket-Keeper": "Wicketkeeper",
        "Batter": "Batsman"
    }
)

# some disbanded, some absorbed, some rebranded
team_change_map = {
    "Kings XI Punjab": "Punjab Kings",
    "Delhi Daredevils": "Delhi Capitals",
    "Rising Pune Supergiants": "Rising Pune Supergiant",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru"
}
merge_auction["Team"] = merge_auction["Team"].replace(team_change_map)


print("Merge done!")

time.sleep(3)
print("Getting ready")
###############################################################
############################################################### 
#  Aim - 3NF
# Stage I - Normalise the IPL franchise teams


# Create the team lookup table: each franchise name is stored once with its primary key.
df_teams = pd.DataFrame(teams_data)
df_teams.insert(0, "Team_ID", range(1, len(df_teams) + 1))

# Save the lookup separately so Team_ID values in the auction data can be interpreted.
df_teams.to_csv(OUTPUT_PATH_CLEANED / "teams.csv", index=False)

# Replace repeated team names with the matching foreign key from the lookup table.
team_map = df_teams.set_index("Team")["Team_ID"]
merge_auction["Team_ID"] = (
    merge_auction["Team"].map(team_map).astype("int64")
)

# Stage II - League, but we don't add it to the players auction table. Will break 3NF otherwise

df_leagues = pd.DataFrame(league_data)
df_leagues.insert(0, "League_ID", range(1, len(df_leagues) + 1))
df_leagues.to_csv(OUTPUT_PATH_CLEANED / "leagues.csv", index=False)

# Stage III - Remove the unused player origin field
merge_auction = merge_auction.drop(columns=["Player Origin"])

# Also do the same for currency type but we won't add it, since it violates 3NF,
# Why? Because the league table already has a currency_ID, and its transitive dependancy
df_currency = pd.DataFrame(sold_in_currency)
df_currency.insert(0, "Currency_ID", range(1, len(df_currency) + 1))
df_currency.to_csv(OUTPUT_PATH_CLEANED / "currency.csv", index=False)


# Stage IV - Normalise player role

# Create and save the role lookup so role categories have a single definition
df_roles = pd.DataFrame(player_role)
df_roles.insert(0, "Role_ID", range(1, len(df_roles) + 1))
df_roles.to_csv(OUTPUT_PATH_CLEANED / "player_roles.csv", index=False)

# Replace the repeated role label with its lookup key
role_map = df_roles.set_index("Role")["Role_ID"]
merge_auction["Role_ID"] = merge_auction["Role"].map(role_map).astype("int64")
merge_auction = merge_auction.drop(columns=["Role"])

# Keep only the needed auction fields with foreign keys replacing the repeated labels
#This is the final check before outputting
merge_auction.insert(0, "Auction_ID", range(1, len(merge_auction) + 1))
cols = ["Auction_ID", "Player", "Role_ID", "Amount", "Team_ID", "Year"]
merge_auction = merge_auction[cols]
# Output the normalized auction table (IPL only so far).
merge_auction.to_csv(OUTPUT_PATH_CLEANED / "merged_auction_data_nf.csv", index=False)


print("All done - I hope :)")
print("Deliverables:")
print("- teams.csv - dimension table for IPL franchises")
print("- leagues.csv - dimension table for the 3 leagues in scope")
print("- player_roles.csv - dimension table for player roles")
print("- currency.csv - dimension table for currency types")
print("- merged_auction_data_nf.csv - merged auction data")

print("Getting ready for stage 2, player extraction - Expect my arrival, worm")
time.sleep(2)
print("Commencing...")

subprocess.run(
    [sys.executable, str(Path(__file__).resolve().with_name("player_table.py"))],
    check=True)