import docx
from PyPDF2 import PdfReader
import pandas as pd
from typing import List


def read_docx_as_single_page(docx_path: str) -> str:
    doc = docx.Document(docx_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


def read_pdf_as_single_page(pdf_path: str) -> str:
    with open(pdf_path, "rb") as f:
        pdf_reader = PdfReader(f)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            # Extract text from the current page and append it to the string
            text += pdf_reader.pages[page_num].extract_text()
        return text
    
def read_csv_file(file_path: str, max_characters: int = 200) -> List[str]: 
    df = pd.read_csv(file_path)
    text_data = []
    helper_string = ""
    for index, row in df.iterrows():
                
        rooms = row['Rooms']
        compss = row['Competitions']
        time = row['Time']
        day = row['Day']
        text_info = (
            f"Here's information for '{rooms}' venue: \n"
            f"- Competition: '{compss}' are going to be held here\n"
            f"- Their timings are '{time} PM' \n"
            f"- It will be held on the day '{day}'\n"
        )
        #print(len(text_info))
        spaces = ' ' * (max_characters - len(text_info)) if len(text_info) < max_characters else ''
        text_info += spaces
        print(len(text_info))
        helper_string += text_info
        text_data.append(text_info)
    return text_data

#print(read_csv_file("/home/k224575/Desktop/test/codes/probot/Procom-ChatBot-Automation/document_vectorization/data_gen/csvs/Day_1 Competitions.csv"))