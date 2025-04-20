# # import re
# import json
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.schema import HumanMessage
# import answer_extraction
# import os

# load_dotenv()  # Uncomment this line
# # api_key = os.getenv("GOOGLE_API_KEY") 

# def grade_all_answers(student_answers, marking_scheme):
#     model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)

#     prompt = f"""
# You are an experienced examiner. Grade the student's answers based on the provided marking scheme. 
# For each question, return a JSON with:
# - `total_awarded`: Total marks given
# - `steps`: A list of steps with `keyword`, `expected_marks`, and `awarded_marks`
# - If the student didn't answer, return 0 marks and an empty steps list

# Format:
# {{
#   "Q1": {{
#     "total_awarded": ...,
#     "steps": [{{"keyword": "...", "expected_marks": ..., "awarded_marks": ...}}, ...]
#   }},
#   ...
# }}

# Marking Scheme:
# {json.dumps(marking_scheme, indent=2)}

# Student Answers:
# {student_answers}
# """

#     result = model.invoke([HumanMessage(content=prompt)])
#     return result.content
    
#     # try:
#     #     return json.loads(result.content)
#     # except json.JSONDecodeError:
#     #     print("[ERROR] Failed to parse Gemini output.")
#     #     return {"error": "JSON parsing failed", "raw_response": result.content}


# marking_scheme = {
#     "Q1": {
#         "total_marks": 5,
#         "steps": [
#             {"keyword": "Definition of photosynthesis", "marks": 1},
#             {"keyword": "Sunlight or chlorophyll", "marks": 1},
#             {"keyword": "Products formed", "marks": 1},
#             {"keyword": "Explanation of process", "marks": 1},
#             {"keyword": "Diagram", "marks": 1}
#         ]
#     },
#     "Q2": {
#         "total_marks": 5,
#         "steps": [
#             {"keyword": "Three states", "marks": 2},
#             {"keyword": "Examples for each", "marks": 3}
#         ]
#     },
#     "Q3": {
#         "total_marks": 5,
#         "steps": [
#             {"keyword": "Stages of water cycle", "marks": 3},
#             {"keyword": "Diagram", "marks": 2}
#         ]
#     },
#     "Q4": {
#         "total_marks": 5,
#         "steps": [
#             {"keyword": "Safety Measure 1", "marks": 1},
#             {"keyword": "Safety Measure 2", "marks": 1},
#             {"keyword": "Safety Measure 3", "marks": 1},
#             {"keyword": "Safety Measure 4", "marks": 1},
#             {"keyword": "Relevance", "marks": 1}
#         ]
#     }
# }

# # 4. Simulated PDF answer text (replace with extracted text)
# pdf_text = """
# Q1. Photosynthesis is how plants make food using sunlight. They take in carbon dioxide and water, and produce oxygen and glucose.

# Q2. Three states are solid, liquid and gas. Ice is solid, water is liquid and steam is gas.

# Q4. Safety during earthquakes includes staying calm, taking cover, avoiding windows and helping others.
# """

# # 5. Extract answers and grade all at once
# student_answers = answer_extraction.extract_student_scipts(pdf_text)
# final_grades = grade_all_answers(student_answers, marking_scheme)

# # 6. Output final grading result
# # print(json.dumps(final_grades, indent=2))
# print(final_grades)







# # Example usage
# if __name__ == "__main__":
#     sample_marking_scheme = {
#         "Q1": {
#             "total_marks": 4,
#             "keywords": ["Correct negation for part (a)", "Correct negation for part (b)", "Correct negation for part (c)"],
#             "marks_distribution": [1, 1, 2]
#         }
#     }
#     pdf_text = """
# Q1. Photosynthesis is how plants make food using sunlight. They take in carbon dioxide and water, and produce oxygen and glucose.

# Q2. Three states are solid, liquid and gas. Ice is solid, water is liquid and steam is gas.

# Q4. Safety during earthquakes includes staying calm, taking cover, avoiding windows and helping others.
# """


#     marking_scheme = {
#     "Q1": {
#         "total_marks": 5,
#         "steps": [
#             {"keyword": "Definition of photosynthesis", "marks": 1},
#             {"keyword": "Sunlight or chlorophyll", "marks": 1},
#             {"keyword": "Products formed", "marks": 1},
#             {"keyword": "Explanation of process", "marks": 1},
#             {"keyword": "Diagram", "marks": 1}
#         ]
#     },
#     "Q2": {
#         "total_marks": 5,
#         "steps": [
#             {"keyword": "Three states", "marks": 2},
#             {"keyword": "Examples for each", "marks": 3}
#         ]
#     },
#     "Q3": {
#         "total_marks": 5,
#         "steps": [
#             {"keyword": "Stages of water cycle", "marks": 3},
#             {"keyword": "Diagram", "marks": 2}
#         ]
#     },
#     "Q4": {
#         "total_marks": 5,
#         "steps": [
#             {"keyword": "Safety Measure 1", "marks": 1},
#             {"keyword": "Safety Measure 2", "marks": 1},
#             {"keyword": "Safety Measure 3", "marks": 1},
#             {"keyword": "Safety Measure 4", "marks": 1},
#             {"keyword": "Relevance", "marks": 1}
#         ]
#     }
# }

    
#     sample_student_answers = "Q1: (a) ¬(p ∧ q) ≡ ¬p ∨ ¬q, (b) ¬(p ∨ q) ≡ ¬p ∧ ¬q, (c) ¬(p → q) ≡ p ∧ ¬q"
    
#     result = grade_all_answers(pdf_text, marking_scheme)
    
#     # Save result to file
#     with open("results.json", "w") as file:
#         file.write(result)
    
#     print("Grading completed and saved to results.json")










# import json
# import re
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.schema import HumanMessage
# import os

# load_dotenv()

# def grade_all_answers(student_answers, marking_scheme):
#     model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)

#     prompt = f"""
# You are an experienced examiner. Grade the student's answers based on the provided marking scheme. 
# For each question, return a JSON with:
# - `total_awarded`: Total marks given
# - `steps`: A list of steps with `keyword`, `expected_marks`, and `awarded_marks`
# - If the student didn't answer, return 0 marks and an empty steps list

# Format:
# {{
#   "Q1": {{
#     "total_awarded": ...,
#     "steps": [{{"keyword": "...", "expected_marks": ..., "awarded_marks": ...}}, ...]
#   }},
#   ...
# }}

# Your response should be valid JSON only, with no additional text before or after the JSON structure.

# Marking Scheme:
# {json.dumps(marking_scheme, indent=2)}

# Student Answers:
# {student_answers}
# """

#     result = model.invoke([HumanMessage(content=prompt)])
#     raw_content = result.content
    
#     # Extract JSON from the model's response
#     # First, try to find JSON between code blocks
#     json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', raw_content, re.DOTALL)
    
#     if json_match:
#         json_content = json_match.group(1)
#     else:
#         # If no code blocks, try to use the entire content
#         json_content = raw_content
    
#     # Clean content by removing non-JSON text
#     # Look for content that appears to be JSON (starts with { and ends with })
#     clean_match = re.search(r'(\{.*\})', json_content, re.DOTALL)
#     if clean_match:
#         json_content = clean_match.group(1)
    
#     try:
#         # Parse the JSON to ensure it's valid
#         parsed_json = json.loads(json_content)
        
#         # Return proper JSON string
#         return json.dumps(parsed_json, indent=2)
#     except json.JSONDecodeError as e:
#         # If JSON parsing fails, return error message
#         return json.dumps({
#             "error": f"Failed to parse JSON response: {str(e)}",
#             "raw_response": raw_content
#         }, indent=2)


# import json
# import re
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.schema import HumanMessage
# import os

# load_dotenv()

# def grade_all_answers(student_answers, marking_scheme):
#     """
#     Grade all answers based on the marking scheme with context isolation
#     """
#     # Create a new model instance for each evaluation
#     # This ensures there's no state carried over from previous evaluations
#     model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
    
#     # Build a detailed structured prompt to avoid ambiguity
#     prompt = f"""
# You are an experienced examiner. Grade the student's answers based on the provided marking scheme.
# For each question in the marking scheme, you must return a result in this exact structure:
# {{
#   "Q1": {{
#     "total_awarded": <number>,
#     "steps": [
#       {{"keyword": "<criterion>", "expected_marks": <number>, "awarded_marks": <number>}},
#       ...
#     ]
#   }},
#   "Q2": {{
#     "total_awarded": <number>,
#     "steps": [
#       ...
#     ]
#   }},
#   ...and so on for each question
# }}

# Important requirements:
# 1. Your response must be ONLY valid JSON with no other text
# 2. Use exactly the question numbers from the marking scheme (Q1, Q2, etc.)
# 3. If a student didn't answer a question, set total_awarded to 0 with empty steps array for that question
# 4. Ensure all questions from the marking scheme are included in your response
# 5. The output MUST contain ALL questions from Q1 to Q{len(marking_scheme)} in exact order

# Marking Scheme:
# {json.dumps(marking_scheme, indent=2)}

# Student Answers:
# {json.dumps(student_answers, indent=2)}
# """

#     # Make the API call with complete isolation
#     result = model.invoke([HumanMessage(content=prompt)])
#     raw_content = result.content
    
#     # Clean and extract the JSON
#     # First, try to find JSON between code blocks
#     json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', raw_content, re.DOTALL)
    
#     if json_match:
#         json_content = json_match.group(1)
#     else:
#         # If no code blocks, try to use the entire content
#         json_content = raw_content
    
#     # Look for content that appears to be JSON (starts with { and ends with })
#     clean_match = re.search(r'(\{.*\})', json_content, re.DOTALL)
#     if clean_match:
#         json_content = clean_match.group(1)
    
#     try:
#         # Parse and validate the JSON
#         parsed_json = json.loads(json_content)
        
#         # Ensure all questions from marking scheme are included
#         for question_id in marking_scheme.keys():
#             if question_id not in parsed_json:
#                 parsed_json[question_id] = {
#                     "total_awarded": 0,
#                     "steps": []
#                 }
        
#         # Sort the questions to maintain consistent order
#         sorted_result = {question_id: parsed_json[question_id] 
#                          for question_id in sorted(parsed_json.keys())}
        
#         # Return properly formatted JSON
#         return json.dumps(sorted_result, indent=2)
#     except json.JSONDecodeError as e:
#         # If JSON parsing fails, return error message
#         return json.dumps({
#             "error": f"Failed to parse model response: {str(e)}",
#             "raw_response": raw_content[:500]  # Include first 500 chars of response for debugging
#         }, indent=2)


# import json
# import re
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.schema import HumanMessage
# import os

# load_dotenv()

# def grade_all_answers(student_answers, marking_scheme):
#     model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)

#     prompt = f"""
# You are an experienced examiner. Grade the student's answers based on the provided marking scheme. 
# For each question, return a JSON with:
# - `total_awarded`: Total marks given
# - `steps`: A list of steps with `keyword`, `expected_marks`, and `awarded_marks`
# - If the student didn't answer, return 0 marks and an empty steps list

# Format:
# {{
#   "Q1": {{
#     "total_awarded": ...,
#     "steps": [{{"keyword": "...", "expected_marks": ..., "awarded_marks": ...}}, ...]
#   }},
#   ...
# }}

# Your response should be valid JSON only, with no additional text before or after the JSON structure.

# Marking Scheme:
# {json.dumps(marking_scheme, indent=2)}

# Student Answers:
# {student_answers}
# """

#     result = model.invoke([HumanMessage(content=prompt)])
#     raw_content = result.content
    
#     # Extract JSON from the model's response
#     # First, try to find JSON between code blocks
#     json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', raw_content, re.DOTALL)
    
#     if json_match:
#         json_content = json_match.group(1)
#     else:
#         # If no code blocks, try to use the entire content
#         json_content = raw_content
    
#     # Clean content by removing non-JSON text
#     # Look for content that appears to be JSON (starts with { and ends with })
#     clean_match = re.search(r'(\{.*\})', json_content, re.DOTALL)
#     if clean_match:
#         json_content = clean_match.group(1)
    
#     try:
#         # Parse the JSON to ensure it's valid
#         parsed_json = json.loads(json_content)
        
#         # Return proper JSON string
#         return json.dumps(parsed_json, indent=2)
#     except json.JSONDecodeError as e:
#         # If JSON parsing fails, return error message
#         return json.dumps({
#             "error": f"Failed to parse JSON response: {str(e)}",
#             "raw_response": raw_content
#         }, indent=2)

# # Example usage
# if __name__ == "__main__":
#     sample_marking_scheme = {
#         "Q1": {
#             "total_marks": 4,
#             "keywords": ["Correct negation for part (a)", "Correct negation for part (b)", "Correct negation for part (c)"],
#             "marks_distribution": [1, 1, 2]
#         }
#     }
    
#     sample_student_answers = "Q1: (a) ¬(p ∧ q) ≡ ¬p ∨ ¬q, (b) ¬(p ∨ q) ≡ ¬p ∧ ¬q, (c) ¬(p → q) ≡ p ∧ ¬q"
    
#     result = grade_all_answers(sample_student_answers, sample_marking_scheme)
    
#     # Save result to file
#     with open("results.json", "w") as file:
#         file.write(result)
    
#     print("Grading completed and saved to results.json")


import json
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import os

load_dotenv()

def grade_all_answers(student_answers, marking_scheme):
    # Create a fresh instance of the model (stateless)
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0
    )

    # Full standalone prompt (no reliance on previous state)
    prompt = f"""
You are an experienced examiner. Grade the student's answers based on the provided marking scheme.

Return a strict JSON object per question in the format:
{{
  "Q1": {{
    "total_awarded": <number>,
    "steps": [
      {{
        "keyword": "<expected keyword>",
        "expected_marks": <number>,
        "awarded_marks": <number>
      }},
      ...
    ]
  }},
  ...
}}

Rules:
- If a question is unanswered, set `total_awarded` to 0 and `steps` to an empty list.
- Your output must be **valid JSON only**, with no explanation or extra commentary.

Marking Scheme:
{json.dumps(marking_scheme, indent=2)}

Student Answers:
{student_answers}
"""

    # Send the prompt as a completely fresh message
    result = model.invoke([HumanMessage(content=prompt)])
    raw_content = result.content

    # Attempt to extract JSON from code block or full text
    json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', raw_content, re.DOTALL)
    json_content = json_match.group(1) if json_match else raw_content

    # Clean up by matching JSON format directly
    clean_match = re.search(r'(\{.*\})', json_content, re.DOTALL)
    if clean_match:
        json_content = clean_match.group(1)

    try:
        parsed_json = json.loads(json_content)
        return json.dumps(parsed_json, indent=2)
    except json.JSONDecodeError as e:
        return json.dumps({
            "error": f"Failed to parse JSON response: {str(e)}",
            "raw_response": raw_content
        }, indent=2)
