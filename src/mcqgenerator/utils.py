import os
import PyPDF2
import json
import traceback

def read_file(file_path):
    if file_path.name.endswith('.pdf'):
        try:
            pdf_reader=PyPDF2.PdfFileReader(file_path)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        except Exception as e:
            raise Exception("Error reading PDF file")
    
    elif file_path.name.endswith('.txt'):
        return file_path.read().decode('utf-8')
    
    else:
        raise Exception(
            "Unsupported files, Application supported with only PDf and text files"
        )
    
def get_table_data(quiz_str):
    try:
        quiz_dict=json.loads(quiz_str)
        quiz_table_data=[]
        
        for key, value in quiz_dict.items():
            mcq=value['mcq']
            options='||'.join(
               [
                    f"{option} -> {option_value}" for option, option_value in value["options"].items()
               ]
            )

            correct=value['correct']
            quiz_table_data.append({
                "MCQ":mcq,
                "Choices":options,
                "Correct":correct
            })

        return quiz_table_data
    
    except Exception as e:
        traceback.print_exception(type(e), e,e.__traceback__)
        return False
               