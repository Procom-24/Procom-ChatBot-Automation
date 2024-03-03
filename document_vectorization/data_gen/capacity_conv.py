import pandas as pd
import os

csv_file_path = './csvs/Capacity.csv'

df = pd.read_csv(csv_file_path)

text_data = []

for index, row in df.iterrows():
    competition = row['Competitions']
    cap_teams = (str(row['CAP(Teams)']))
    day1_allocation = str(row['Lab/Room Allocated Day 1 '])
    day2_allocation = str(row['Lab/Room Allocated Day 2'])

    # text_info = f"Competition: {competition}\nCAP Teams: {cap_teams}\nDay 1 Allocation: {day1_allocation}\nDay 2 Allocation: {day2_allocation}\n"
    text_info = (
        f"Here's the information for the '{competition}' competition:\n"
        f"- CAP Teams: {(cap_teams)}\n"
        f"- Lab/Room Allocated on Day 1: {day1_allocation}\n"
        f"- Lab/Room Allocated on Day 2: {day2_allocation}\n"
    )

    text_data.append(text_info)



os.makedirs('txts', exist_ok=True)
output_file_path = './txts/Capacity.txt'

with open(output_file_path, 'w') as file:
    file.write('\n'.join(text_data))

print(f"Text data has been written to '{output_file_path}'")
