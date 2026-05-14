import os
import re
import json
import pandas as pd
import traceback

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.callbacks import get_usage_metadata_callback
from langchain_core.runnables import RunnablePassthrough
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
import PyPDF2
import streamlit as st

with open(r'C:\Users\hp\mcqgen1\Response.json','r') as file:
    RESPONSE_JSON=json.load(file)

    type(RESPONSE_JSON)

st.title("MCQS Creator Application with Langchain")

with st.form("user_inputs"):
    uploaded_file=st.file_uploader("upload a PDF or text file")

    mcq_count= st.number_input("No of MCQs", min_value=3, max_value=50)

    subject=st.text_input("Insert Subject",max_chars=20)

    tone=st.text_input("Complexity Level of Questions", max_chars=20, placeholder="Simple")

    button=st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and  mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text=read_file(uploaded_file)
                with get_usage_metadata_callback() as cb:
                    response=generate_evaluate_chain.invoke(
                         {
        
                   "text":text,
                   "number":mcq_count,
                   "subject":subject,
                   "tone":tone,
                   "response_json":json.dumps(RESPONSE_JSON, indent=2)
                        })
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")
            else:
            
                if isinstance(response,dict):
                    quiz=response.get("quiz", None)
                    table_data=get_table_data(quiz)
                    if table_data is not None:
                        df=pd.DataFrame(table_data)
                        df.index=df.index+1
                        st.table(df)
                        st.text_area(label="Review",value=response["review"])
                    else:
                        st.error("Error in the table data")
                else:
                    st.write(response)
                