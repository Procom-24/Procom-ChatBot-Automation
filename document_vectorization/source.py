
import chromadb
import openai
from chromadb.utils import embedding_functions
from langchain.document_loaders import TextLoader
import os
from typing import List
import pandas as pd
import docx
import data_collectors as dt
from PyPDF2 import PdfReader


max_characters = 200

# folder_name = 'procom_data'
document = []
metadata = []

import os

def list_files(folder_path):
    """
    List all files inside the specified folder and its subfolders.
    
    Args:
    - folder_path: The path of the folder to search.
    
    Returns:
    - file_paths: A list containing the paths of all files found.
    """
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths


folder_name = "data_gen"
folders = ['csvs', 'txts', "pdfs", "docxs"]

for folder in folders:
    folder_path = os.path.join(folder_name, folder)
    files = list_files(folder_path)
    for file in files:
            
            # Get the file name for metadata.
        file_name = file.split('.')[0]
            
        text = "" ##Using an Empty string, to save data as text(String) and appending it to documents list.

            # If the file is a PDF then process it with "read_pdf_as_single_page".
            # Elif the file is a PDF then process it with "read_docx_as_single_page".
            # Elif if the file ends with .csv, then read the 
            # ELse process it with "TextLoader".

            #Not appending the document, and metadata variable at the beginning due to the CSV File case, 
            #where I will be splitting the data into chunks(5-6) and then proceed to feed it to DB

            # Finally append the text string to the document list and the file name into metadata list.

        if file.endswith(".pdf"):
            
            #pdf_path = f"./{folder_name}/" + file
            text = dt.read_pdf_as_single_page(file)

            
            metadata.append({"competition" : file_name })
            document.append(text)
            
        elif file.endswith(".docx") or file.endswith(".doc"):
            
            #doc_path = f"./{folder_name}/" + file
            text = dt.read_docx_as_single_page(file) 
            
            metadata.append({"competition" : file_name })
            document.append(text)
            
        elif file.endswith(".txt"):
            text = ""
            #txt_path = f"./{folder_name}/" + file
            #loader = TextLoader(file)
            with open(file, "r") as file:
                text = file.read()
            
            document.append(text)
            metadata.append({"competition" : file_name }) 
            
        elif file.endswith("Competitions.csv"): #Added this function, reads CSV file.
                
            #file_path = f"./{folder_name}/" + file
            # if file.endswith("Competitions.csv"): #Have formatted both CSV Files of Day 1 and Day 2 in such a way that they both contain necessary data.
            text = dt.read_csv_file(file, max_characters=max_characters)
            
            for i, chunks in enumerate(text):
                document.append(chunks)
                metadata.append({"competition" : file_name + str(i + 1)})



chroma_client = chromadb.PersistentClient("./Procom_Database") #Creating a chroma client
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")



#API KEY and Embeddings Setup
OPEN_AI_API_KEY = "OPENAI API KEY"
embedding_model = "text-embedding-ada-002"
openai_client = openai.OpenAI(api_key='eee')

# This is OpenAI embedding function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPEN_AI_API_KEY,
    model_name=embedding_model,
)

#Creating a collection in chroma
collection = chroma_client.get_or_create_collection( 
    name="procom_dataset123", embedding_function=sentence_transformer_ef
)


#Inserting the data that i retreived from files into the database, file by file or chunk-by-chunk
for i, text in enumerate(document):
   collection.add(documents = document[i], metadatas=metadata[i], ids=[str(i)])

resp = collection.query(query_texts="Tell me the rules of App dev", n_results=2)
print(resp['documents'][0])

# def get_embedding(text: str, model: str = "text-embedding-ada-002") -> List[float]:
#     text = text.replace("\n", " ")
#     return openai_client.embeddings.create(input=[text], model=model).data[0].embedding


# def ask_procom_chatbot(user_query: str) -> str:
#     # Generate an embedded query from user query.
#     embedded_query = get_embedding(user_query, model=embedding_model)

#     # Retrieve all relevant data to teh user query
#     all_relevant_info = collection.query(
#         query_embeddings=embedded_query,
#         n_results=1,
#     )

#     # Separating and concatenating the retrieved data.
#     query_set = all_relevant_info["documents"][0]
#     query_respond = "\n".join(str(item) for item in query_set)

#     # Send the all info to the chatbot
#     chatbot_response = ask_openai(user_query, query_respond)
#     return chatbot_response


# def ask_openai(user_query: str, query_respond: str) -> str:
#     system_prompt = f"""
#         You are an informative chatbot specifically made for 
#         an event called PROCOM. Your task is to answer user 
#         questions based solely on the provided information. You can not answer the 
#         user query from your knowledge. If the user's query is
#         within the scope of the provided information, you 
#         will provide an answer. However, if the query is not 
#         relevant to the information provided, you will politely inform the user
#         that it's out of your knowledge.
#         Below is the available information:
#         There are a total of 19 competitions listed below in Procom:
#         AI Showdown, App Dev, Blockchain Blitz, Chatcraft, Code In The Dark, 
#         Code Sprint, Competitive Programming, CTF, Database Design, Game Dev,
#         Hackathon, LFR Rules, Psuedo War, ROBO SOCCER Rules, ROBO SUMO Rules, 
#         ROBO WAR(Light Weight) Rules, Speed Debugging, UIUX, and Web Dev.
#         INFORMATION  
#         ####
#         {query_respond}
#         ####
#         Your response must be easy for user to understand.
#     """

#     messages = [
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": user_query},
#     ]

#     response = openai_client.chat.completions.create(
#         model="gpt-3.5-turbo", messages=messages, temperature=0
#     )

#     response_message = response.choices[0].message.content
#     return response_message



# #Main Work
# user_input = "What are the rules of Robo Soccer?"

# procom_chatbot_response = ask_procom_chatbot(user_input)
# print(procom_chatbot_response)
