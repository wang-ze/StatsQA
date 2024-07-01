import os
import PyPDF2
import json
import traceback


def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfFileReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
            
        except Exception as e:
            raise Exception("error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "unsupported file format only pdf and text file suppoted"
            )


def extract_between_braces(s):
    start = s.find('{')
    # Ensure the character after the first '{' is not another '{'
    while start != -1 and start + 1 < len(s) and s[start + 1] == '{':
        start = s.find('{', start + 1)
    
    end = s.rfind('}')
    # Ensure the character before the last '}' is not another '}'
    while end != -1 and end - 1 >= 0 and s[end - 1] == '}':
        end = s.rfind('}', 0, end - 1)
    
    if start != -1 and end != -1 and end > start:
        return "{" + s[start+1:end] + "}}"
    return ""



def get_table_data(all_result):
    try:
        quiz_str = all_result.get("quiz").content
        quiz_str = extract_between_braces(quiz_str)
        # convert the quiz from a str to dict
        quiz_dict=json.loads(quiz_str)
        quiz_table_data=[]
        
        # iterate over the quiz dictionary and extract the required information
        for key,value in quiz_dict.items():
            STATSQA = value["STATSQA"]
            options = " | ".join(
                [
                    f"{option}: {option_value}"
                    for option, option_value in value["options"].items()
                    ]
        )
            correct = value["correct"]
            quiz_table_data.append({"STATSQA": STATSQA, "Choices": options, "Correct": correct})
        
        return quiz_table_data
        
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False


