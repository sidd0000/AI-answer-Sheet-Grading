import re
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()

def extract_marking_scheme(text):
    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)

    prompt = f"""
You are an expert teaching assistant. Break down the following marking scheme into a JSON format with `steps`, each having a `keyword` and `marks`.
Distribute the marks fairly based on the content.

Expected output format:
{{
  "Q1": {{
    "total_marks": <int>,
    "steps": [{{"keyword": "<step name>", "marks": <float>}}, ...]
  }},
  ...
}}

Marking scheme to convert:
\"\"\"{text}\"\"\"
"""

    result = model.invoke([HumanMessage(content=prompt)])
    raw_content = result.content.strip()

    # Step 1: Try extracting JSON from code blocks
    json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', raw_content, re.DOTALL)
    json_content = json_match.group(1) if json_match else raw_content

    # Step 2: Look for valid JSON inside response
    clean_match = re.search(r'(\{.*\})', json_content, re.DOTALL)
    if clean_match:
        json_content = clean_match.group(1)

    # Step 3: Attempt to parse it
    try:
        parsed = json.loads(json_content)
        return json.dumps(parsed, indent=2)
    except json.JSONDecodeError as e:
        return json.dumps({
            "error": "Failed to parse JSON response",
            "details": str(e),
            "raw_response": raw_content
        }, indent=2)

    # return json.loads(result.content)  # ✅ Parse JSON string to Python dict

  
  
 
# marking_scheme_text = """ Q1. Define Photosynthesis. Explain the process with the help of a diagram. Mention the main products formed.
# Total Marks: 5
# Q2. What are the three states of matter? Explain each with an example.
# Total Marks: 4
# Q3. Explain the water cycle with the help of a diagram.
# Total Marks: 5
# Q4. List and explain any four safety measures during an earthquake.
# Total Marks: 4"""

# result = extract_marking_scheme(marking_scheme_text)
# print(result)





