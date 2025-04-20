# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import HumanMessage
# from dotenv import load_dotenv

# load_dotenv()

# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-pro",
#     google_api_key="AIzaSyCCW7pWc3SFp5y0Xl-s7BM2EgcHifweQbU"
# )

# result = llm.invoke([
#     HumanMessage(content="What is the capital of France?")
# ])
# print(result.content)



from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def show_results():
    json_data = '''
    {
      "Q1": {
        "total_awarded": 4,
        "steps": [
          {"keyword": "Correct negation for part (a)", "expected_marks": 1, "awarded_marks": 1},
          {"keyword": "Correct negation for part (b)", "expected_marks": 1, "awarded_marks": 1},
          {"keyword": "Correct negation for part (c)", "expected_marks": 2, "awarded_marks": 2}
        ]
      },
      "Q2": {
        "total_awarded": 10,
        "steps": [
          {"keyword": "Correct equivalence for part (a)", "expected_marks": 1.5, "awarded_marks": 1.5},
          {"keyword": "Correct equivalence for part (b)", "expected_marks": 1.5, "awarded_marks": 1.5},
          {"keyword": "Correct equivalence for part (c)", "expected_marks": 1.5, "awarded_marks": 1.5},
          {"keyword": "Correct equivalence for part (d)", "expected_marks": 1.5, "awarded_marks": 1.5},
          {"keyword": "Correct equivalence for part (e)", "expected_marks": 1.5, "awarded_marks": 1.5},
          {"keyword": "Correct equivalence for part (f)", "expected_marks": 1.5, "awarded_marks": 1.5},
          {"keyword": "Correct equivalence for part (g)", "expected_marks": 1, "awarded_marks": 1},
          {"keyword": "Correct equivalence for part (h)", "expected_marks": 1, "awarded_marks": 1}
        ]
      }
    }
    '''
    data = json.loads(json_data)
    return render_template('result.html', data=data)
