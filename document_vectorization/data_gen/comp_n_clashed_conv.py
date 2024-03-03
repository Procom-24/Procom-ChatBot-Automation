import pandas as pd
import os

csv_file_path = './csvs/Competitons & Classes D1.csv'

df = pd.read_csv(csv_file_path, skiprows=1) # To skip Day1 wali row

text_data = []

for index, row in df.iterrows():
    room = row['Rooms']
    competition_1 = str(row['Competition'])
    time_1 = str(row['Time'])
    competition_2 = str(row['Competition_2'])
    time_2 = str(row['Time_2'])
    
    print(room, type(room))
    
    if pd.isna(room) :# and competition_1 == "" and competition_2 == "" and time_1 == "" and time_2 == "":
        print("---------")
        continue
    
    if competition_1.lower() == 'free':
        competition_1 = 'Free'
        time_1 = 'Free'
    
    if competition_2.lower() == 'free':
        competition_2 = 'Free'
        time_2 = 'Free'

    text_info = (
        f"Here's the schedule for Room '{room}' on Day 1:\n"
        f"- Competition 1: {competition_1} | Time: {time_1}\n"
        f"- Competition 2: {competition_2} | Time: {time_2}\n"
    )

    text_data.append(text_info)

os.makedirs('txts', exist_ok=True)
output_file_path = './txts/Competitons & Classes D1.txt'

with open(output_file_path, 'w') as file:
    file.write('\n'.join(text_data))

print(f"Text data has been written to '{output_file_path}'")
