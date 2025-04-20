# import os
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import HumanMessage
# from dotenv import load_dotenv

# load_dotenv()

# def extract_text_from_base64_image(image_base64: str, prompt: str = "Extract all the text clearly from this image or pdf uploaded.") -> str:
#     """
#     Extracts text from a base64-encoded image using Gemini Vision.
    
#     Args:
#         image_base64 (str): Base64 encoded image data.
#         prompt (str): Prompt for the model.
        
#     Returns:
#         str: Extracted text from the image.
#     """
#     llm = ChatGoogleGenerativeAI(model="gemini-pro-vision", temperature=0)

#     message = HumanMessage(
#         content=[
#             {"type": "text", "text": prompt},
#             {
#                 "type": "image_url",
#                 "image_url": {
#                     "url": f"data:image/png;base64,{image_base64}"
#                 }
#             }
#         ]
#     )

#     response = llm.invoke([message])
#     return response.content
import base64
import os
from io import BytesIO
from pdf2image import convert_from_bytes, convert_from_path
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

def extract_text_from_base64_pdf(pdf_base64: str, prompt: str = "Extract all the text clearly from this image or pdf.") -> str:
    """
    Extracts text from a base64-encoded PDF by converting each page to image
    and using Gemini Vision to extract text from all pages.

    Args:
        pdf_base64 (str): Base64 encoded PDF data.
        prompt (str): Prompt for the model.

    Returns:
        str: Combined extracted text from all pages of the PDF.
    """
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-pro-vision", temperature=0)

        # Decode base64 PDF
        pdf_bytes = base64.b64decode(pdf_base64)
        
        # Convert PDF pages to images
        images = convert_from_bytes(pdf_bytes)
        
        extracted_text = ""

        for idx, img in enumerate(images):
            # Convert image to base64
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            # Gemini Vision message per page
            message = HumanMessage(
                content=[
                    {"type": "text", "text": f"{prompt} (Page {idx + 1})"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_b64}"
                        }
                    }
                ]
            )

            # Extract text from image using Gemini
            response = llm.invoke([message])
            extracted_text += f"\n--- Page {idx + 1} ---\n{response.content.strip()}\n"

        return extracted_text.strip()
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_text_from_pdf_file(pdf_path: str, prompt: str = "Extract all the text clearly from this image or pdf.") -> str:
    """
    Extracts text from a PDF file by converting each page to image
    and using Gemini Vision to extract text from all pages.

    Args:
        pdf_path (str): Path to the PDF file.
        prompt (str): Prompt for the model.

    Returns:
        str: Combined extracted text from all pages of the PDF.
    """
    try:
        # Check if file exists
        if not os.path.exists(pdf_path):
            return f"Error: File not found at {pdf_path}"
            
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
        
        # Convert PDF pages to images
        images = convert_from_path(pdf_path)
        
        extracted_text = ""

        for idx, img in enumerate(images):
            # Convert image to base64
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            # Gemini Vision message per page
            message = HumanMessage(
                content=[
                    {"type": "text", "text": f"{prompt} (Page {idx + 1})"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_b64}"
                        }
                    }
                ]
            )

            # Extract text from image using Gemini
            response = llm.invoke([message])
            extracted_text += f"\n--- Page {idx + 1} ---\n{response.content.strip()}\n"

        return extracted_text.strip()
    except Exception as e:
        return f"Error extracting text: {str(e)}"

# Example usage:
if __name__ == "__main__":
    # Option 1: Extract text from a file path
    pdf_path = "Tutorial 3 solution.pdf"  # Use the actual file path
    text = extract_text_from_pdf_file(pdf_path)
    print(text)
    
    # Option 2: Extract text from base64 string
    # First, read and encode the PDF file to base64
    with open(pdf_path, "rb") as pdf_file:
        pdf_base64 = base64.b64encode(pdf_file.read()).decode("utf-8")
        text = extract_text_from_base64_pdf(pdf_base64)
        print(text)