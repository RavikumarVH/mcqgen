import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain_community.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain 
from src.mcqgenerator.logger import logging
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

#loading JSON file
with open('Response.json',"r") as file:
    RESPONSE_JSON = json.load(file)


#creating a title for the app
st.title("MCQ Creator Application with Langchain")

with st.form("user_inputs"):
    #file upload
    uploaded_files=st.file_uploader("Upload PDf or Text file")

    #input fields
    mcq_count=st.number_input("No of MCQs", min_value=3, max_value=20)

    #Subject
    subject=st.text_input("Insert Subject", max_chars=30)

    #tone
    tone = st.text_input("Complexity Level of questions", max_chars=20, placeholder="Simple")

    #add button 
    button=st.form_submit_button("Create MCQs")

    #if button is clicked
    if button and uploaded_files is not None and mcq_count and subject and tone:
        with st.spinner("loading.."):
            try:
                text=read_file(uploaded_files)

                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                            "text":text,
                            "number":mcq_count,
                            "subject":subject,
                            "tone":tone,
                            "response_json":RESPONSE_JSON
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e), e,e.__traceback__)
                st.error("Something went wrong")
                st.stop()

            else:
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                if isinstance(response, dict):
                    #extract the quiz data from the response
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data=get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            #display the review in text box as well
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("Something went wrong")
                            st.stop()
                else:
                    st.write(response)
