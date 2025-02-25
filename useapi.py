import requests
import json
import pandas as pd
import re
import requests
import json
import pandas as pd
import re
from typing import *
import os
import json
import pandas as pd
import re
import openai  
from openai import OpenAI
from openai.types.chat.chat_completion import Choice

def read_excel(file_path: str) -> pd.DataFrame:
    return pd.read_excel(file_path, index_col=None, engine='openpyxl')
def parse_json_from_content(content):
    try:
       
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Initial JSON parse failed: {e}") 
        try:
           
            match = re.search(r'\{.*?\}', content, re.DOTALL)
            if match:
                try:
                    result_data = json.loads(match.group())  # Parse the matched JSON array
                    return result_data
                except json.JSONDecodeError:
                    return {}  # Return empty list if JSON decoding fails
            else:
                return {}  # Return empty list if no JSON array found

        except requests.RequestException:
            return {}  # Return empty list if a request exception occurs


client = OpenAI(api_key="",base_url="",)
def openAiProcessText(prompttext):
    try:
        completion = client.chat.completions.create(
            model="moonshot-v1-auto",
            messages=[
                {"role": "system",
                 "content": "You are an excellent geologist."},
                {"role": "user",
                 "content": prompttext
                 }
            ],
            temperature=0.1,
        )
    except openai.BadRequestError as e:
        print(f"API request failed: {e}")
        return  {}

    extracted_data = parse_json_from_content(completion.choices[0].message.content)
    return extracted_data

def main(startindex=0,endindex=0):
    #df = pd.read_excel(r"E:\test.xlsx", index_col=None, engine='openpyxl')

    df = pd.read_excel(r"E:\temp\test.xlsx", index_col=None, engine='openpyxl')
    # df = pd.read_csv('your_file.tsv', sep='\t', header=None)
    result_df = pd.DataFrame()
    save_interval = 50  
    print(df)
    for index, row in df.iterrows():
        if index < startindex:
           continue 
          extracted_data = openAiProcessText("Identify and extract the most precise geological age phrase and geographical location (GPE) from the provided text regarding stromatolites. Analyze the text: "+str(row[1])+". Then, return the data in JSON format {'GeologicalAge': value, 'GPE': location}, where 'value' is the exact geological age phrase found in the text, and 'location' is the geographical location information (if mentioned). Aim for the highest specificity and accuracy based on the given context.")

 extracted_data=extracted_data if isinstance(extracted_data, dict) else {}
       # combined_data = {**{"File_Name": row[0], "Original_Content": row[3],"Formation":row[2],"Time":row[1]}, **extracted_data}
        combined_data = {**{"File_Name": row[0], "Original_Content": row[1]},**extracted_data} 

        result_df = pd.concat([result_df, pd.DataFrame([combined_data])], ignore_index=True)

        if (index - startindex + 1) % save_interval == 0:
        
            result_df.to_excel(f'E://temp2//test_result_{index-save_interval+1}_{index}.xlsx', index=False)
            #result_df = pd.DataFrame() 


    result_df.to_excel(r'E:\final_result.xlsx', index=False)

if __name__ == '__main__':

    main(startindex=1,endindex=9999999)  