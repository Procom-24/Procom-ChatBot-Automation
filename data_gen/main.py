import pandas as pd
import os
def excel_to_csv(input_excel_file, output_csv_folder):
    os.makedirs(output_csv_folder, exist_ok=True)    
    xls = pd.ExcelFile(input_excel_file)

    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)

        output_csv_file = f"{output_csv_folder}/{sheet_name}.csv"

        df.to_csv(output_csv_file, index=False)
        print(f"Sheet '{sheet_name}' saved as '{output_csv_file}'")

# Example usage
input_excel_file = "../data/Procom'24 Plan.xlsx"
output_csv_folder = 'csvs'

excel_to_csv(input_excel_file, output_csv_folder)
