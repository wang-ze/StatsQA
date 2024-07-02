import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.STATSQAGenerator.utils import read_file, extract_between_braces, get_table_data
from src.STATSQAGenerator.logger import logging

#imporing necessary packages packages from langchain
from operator import itemgetter
from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_groq import ChatGroq


# Load environment variables from the .env file
load_dotenv() 

# Access the environment variables just like you would with os.environ
KEY=os.getenv("GROQ_API_KEY")


model = ChatGroq(groq_api_key= KEY, model="llama3-8b-8192")

TEMPLATE="""
Text:{text}
You are an expert STATSQA maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions related to {area} for students in {grade}. 
Make sure the questions are not repeated and format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to generate {number} questions.
### RESPONSE_JSON
{response_json} \

"""
TEMPLATE2="""
You are an expert of English grammar. \
You are given a STATSQA quiz: {quiz} of multiple choice questions related to {area} in statistics.\
You need to evaluate the complexity of the quiz. Use at most 50 words for complexity analysis. \
If the quiz is too easy or too difficult for students in {grade}, 
update the quiz questions to make it more suitable for the students in {grade}.

Check from an expert English Writer of the above quiz:
"""

quiz_generation_prompt = PromptTemplate(
    template=TEMPLATE, 
    input_variables=["text", "number", "area", "grade", "response_json"]
)

#%% 
# quiz_generation_prompt = PromptTemplate.from_template(
#     template=TEMPLATE
# )

quiz_evaluation_prompt = PromptTemplate.from_template(TEMPLATE2)

quiz_generation_chain= quiz_generation_prompt | model
quiz_evaluation_chain = quiz_evaluation_prompt | model


complete_chain = ({
    "text": itemgetter("text"),
    "number": itemgetter("number"),
    "area": itemgetter("area"),
    "grade": itemgetter("grade"),
    "response_json": itemgetter("response_json"),
    "quiz": quiz_generation_chain
    }
    | RunnablePassthrough.assign(eval=quiz_evaluation_chain)
)
