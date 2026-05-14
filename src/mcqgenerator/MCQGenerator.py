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
import PyPDF2
from dotenv import load_dotenv


load_dotenv()
KEY=os.getenv("GROK_API_KEY")

llm=ChatGroq(model="llama-3.1-8b-instant",
            api_key=KEY,
            temperature=0.5,
            )
TEMPLATE="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} muiltiple choice questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to the format your response like RESPONSE_JSON below and use it as a guide.\
Ensure to makw{number} MCQs
### RESPONSE_JSON
{response_json}
"""

quiz_generation_prompt=PromptTemplate(
    input_variables=["text","number","subject","tone","response_json"],
    template=TEMPLATE
)

quiz_chain=quiz_generation_prompt|llm|StrOutputParser()

TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz.Only use at max  50 words for complexity.
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be chnaged and change the tone such that is perfectly fits the students ability.
Quiz_MCQs:
{quiz}

check from an expert English writer of the above quiz:

"""

quiz_evaluation_prompt=PromptTemplate(
    input_variables=["subject","quiz"],
    template=TEMPLATE2
)

review_chain=quiz_evaluation_prompt|llm|StrOutputParser()

from langchain_core.runnables import RunnablePassthrough

generate_evaluate_chain=(
    {"quiz":quiz_chain,"subject":lambda x: x["subject"]}|RunnablePassthrough.assign(review=review_chain)
)