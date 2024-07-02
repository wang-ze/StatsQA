import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.STATSQAGenerator.utils import read_file, extract_between_braces, get_table_data
from src.STATSQAGenerator.logger import logging
import streamlit as st
from src.STATSQAGenerator.STATSQAGenerator import complete_chain



# load the json response file
# dirname = os.getcwd()
# file_path=os.path.join(dirname, "Response.json")
# with open(file_path, 'r') as file:
with open('Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)


# create the title for the streamlit app
st.title('STATS Quiz Generator with Langchain')

# create a form using st.form
with st.form("user_inputs"):
    # upload a file using 
    uploaded_file = st.file_uploader("Upload a PDF or text file", type=["txt", "pdf"])
    # add a number input for the user to input the number of questions
    number = st.number_input("Number of questions", min_value=3, max_value=20)
    # input the specific area
    area = st.text_input(" A topic in Statistics", max_chars=30)
    # add a selectbox for the user to select the grade
    grade = st.selectbox("Grade", ["Elementary School", "Middle School", "High School", "7", "8", "9" ,"10", "11", "12"])
    # add a submit button
    button = st.form_submit_button("Create a Quiz")

if button and uploaded_file is not None and number and area and grade:
    with st.spinner('Generating Quiz...'):
        try:
            text = read_file(uploaded_file)
            # run the complete chain
            all_result = complete_chain.invoke(
                    {
                        "text": text,
                        "number": number,
                        "area": area,
                        "grade": grade,
                        "response_json": json.dumps(RESPONSE_JSON)
                    }
            )       
           # st.write(all_result)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("An error occurred. Please try again.")
        
        else:
            if isinstance(all_result, dict):
                quiz = get_table_data(all_result)
                if quiz is not None:
                    df=pd.DataFrame(quiz)
                    df.index=df.index+1
                    st.table(df)
                    st.text_area(label="Quiz Evaluation", value = all_result.get("eval").content)
                else:
                    st.error("Error: Cannot show quiz questions in a table")


            else:
                st.write(all_result)
            
