# Import necessary libraries
import pandas as pd
import json

# 1) Process match results
with open('t20_wc_match_results.json') as f:
    data = json.load(f)

df_match = pd.DataFrame(data[0]['matchSummary'])

# Display shape and first few rows
print(df_match.shape)
print(df_match.head())

# Rename 'scorecard' column to 'match_id'
df_match.rename({'scorecard': 'match_id'}, axis=1, inplace=True)
print(df_match.head())

# Create match_ids_dict mapping teams to match_id
match_ids_dict = {}
for key, value in df_match.iterrows():
    key1 = value['team1'] + ' Vs ' + value['team2']
    key2 = value['team2'] + ' Vs ' + value['team1']
    match_ids_dict[key1] = match_ids_dict[key2] = value['match_id']

print(match_ids_dict)

# Save match summary to CSV
df_match.to_csv('match_summary.csv', index=False)

# 2) Batting summary
with open('t20_wc_batting_summary.json') as f:
    data = json.load(f)
    
all_records = []
for rec in data:
    all_records.extend(rec['battingSummary'])

df_batting = pd.DataFrame(all_records)

# Add 'out/not_out' column
df_batting['out/not_out'] = df_batting['dismissal'].apply(lambda x: 'out' if len(x) > 0 else 'not_out')

# Drop dismissal column
df_batting.drop(columns=['dismissal'], inplace=True)

# Clean batsman names
df_batting['batsmanName'] = df_batting['batsmanName'].str.replace('â€', '').str.replace('\xa0', '')

# Create 'match_id' column in batting summary
df_batting['match_id'] = df_batting['match'].map(match_ids_dict)

# Save batting summary to CSV
df_batting.to_csv('t20_wc_batting_summary.csv', index=False)

# 3) Bowling summary
with open('t20_wc_bowling_summary.json') as f:
    data = json.load(f)
    
all_records = []
for rec in data:
    all_records.extend(rec['bowlingSummary'])

df_bowling = pd.DataFrame(all_records)

# Create 'match_id' column in bowling summary
df_bowling['match_id'] = df_bowling['match'].map(match_ids_dict)

# Save bowling summary to CSV
df_bowling.to_csv('t20_wc_bowling_summary.csv', index=False)

# 4) Player info
with open('t20_wc_player_info.json') as f:
    data = json.load(f)

df_playerinfo = pd.DataFrame(data)

# Save player info to CSV
df_playerinfo.to_csv('t20_wc_player_info.csv', index = False)
