import re
import json

# def extract_answers_from_text(text, total_questions):
#     answers = {}

#     # This regex matches Q<number> and everything until the next Q<number> or end of text
#     pattern = re.compile(r"(Q\d+)\.?\s*(.*?)(?=Q\d+\.|\Z)", re.DOTALL | re.IGNORECASE)
#     matches = pattern.findall(text)

#     # Build a dictionary from matches
#     match_dict = {q.strip().upper(): ans.strip() for q, ans in matches}

#     # Loop through expected questions and fill answers
#     for i in range(1, total_questions + 1):
#         q_key = f"Q{i}"
#         answer = match_dict.get(q_key.upper(), "").strip()
#         answers[q_key] = answer if answer else "Not Attempted"
    
#     return json.dumps(answers, indent=2) 

# # pdf_text = """Q1. Ideal Answer: Photosynthesis is the process by which green plants prepare food using sunlight, carbon dioxide, and water.
# # It occurs in the chloroplasts of plant cells and involves two major stages: light-dependent reactions and the Calvin cycle.
# # Diagram must include sunlight, chloroplast, CO₂, water, glucose, and oxygen.
# # The main products are glucose (food) and oxygen.

# # q2. Solid – Has a fixed shape and volume (e.g., ice).

# # Liquid – Has a fixed volume but no fixed shape (e.g., water).

# # q4. The water cycle involves:

# # Evaporation: Sun heats water bodies.

# # Condensation: Water vapor forms clouds.

# # Precipitation: Water falls as rain/snow.

# # Collection: Water returns to oceans/rivers. Diagram should include arrows showing the cycle.

# # """

# # result = extract_answers_from_text(pdf_text, total_questions=5)
# # # print(json.dumps(result, indent=2))
# # print(result)



# def extract_answers_from_text(text, total_questions):
#     answers = {}
    
#     # Improved regex that properly captures each question and its answer
#     pattern = re.compile(r"Q(\d+)[\.:]?\s*(.*?)(?=Q\d+[\.:]?|\Z)", re.DOTALL)
#     matches = pattern.findall(text)
    
#     # Build a dictionary from matches
#     for q_num, ans in matches:
#         answers[f"Q{q_num}"] = ans.strip() if ans.strip() else "Not Attempted"
    
#     # Ensure all questions are accounted for
#     for i in range(1, total_questions + 1):
#         q_key = f"Q{i}"
#         if q_key not in answers:
#             answers[q_key] = "Not Attempted"
            
#     return json.dumps(answers, indent=2)



# import re
# import json

# def extract_answers_from_text(text, total_questions):
#     answers = {}
    
#     # Normalize text to make parsing easier
#     # Replace multiple whitespaces with a single space
#     text = re.sub(r'\s+', ' ', text)
    
#     # Find all question-answer pairs with various formats
#     # This pattern looks for question indicators followed by content until the next question
#     pattern = re.compile(r'(?:Q?(\d+)[_\.\):]|\(?(\d+)\))\s*(.*?)(?=(?:Q?(?:\d+)[_\.\):]|\(?(?:\d+)\))|---|\Z)', re.DOTALL)
#     matches = pattern.findall(text)
    
#     for match in matches:
#         # Get question number from either the first or second group (whichever has a value)
#         q_num = match[0] if match[0] else match[1]
#         content = match[2].strip()
        
#         if content:
#             answers[f"Q{q_num}"] = content
#         else:
#             answers[f"Q{q_num}"] = "Not Attempted"
    
#     # Ensure all questions are accounted for
#     for i in range(1, total_questions + 1):
#         q_key = f"Q{i}"
#         if q_key not in answers:
#             answers[q_key] = "Not Attempted"
            
#     return json.dumps(answers, indent=2)



from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import json

load_dotenv()

def extract_student_scipts(text):
    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
    
    prompt = f"""
You are an expert assistant for evaluating student answers.

Given the student's full answer script below, extract answers for each question and present them in a clean JSON format. Follow these rules strictly:

1. Each question key (e.g., "Q1", "Q2", etc.) must be included in the JSON.

2. The value should be the student's response to that question.
3. If a question is **missing or not answered**, mark it as `"Not Attempted"`.
4. Do not add extra explanation or interpretation — only extract the student's actual response.
5. Remove irrelevant text like headers, page numbers, or "Answer:", "Solution:", etc.
6. subparts of the invidual question should be seperated in new line

---

### Example Output Format:
{{
  "Q1": "Student's answer to Q1 \n Subpart 1 answer \n Subpart 2 answer",
  "Q2": "Not Attempted",
  "Q3": "Student's answer to Q3 \n Subpart 1 answer \n Subpart 2 answer",
  ...
}}

Student Asnwer script to convert:
\"\"\"
{text}
\"\"\"


"""
    result = model.invoke([HumanMessage(content=prompt)])
    return result.content
  
  