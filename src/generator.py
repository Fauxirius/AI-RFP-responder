import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.5-flash')

def get_gemini_response(prompt):
    """
    Helper to get response from Gemini.
    """
    try:
        if not api_key:
            return "Error: GOOGLE_API_KEY not found in environment variables."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating content: {str(e)}"

def generate_section(rfp_text, section_name, additional_instructions="", knowledge_base_text="", persona="Standard"):
    """
    Generates a specific section of the offer based on the RFP and Knowledge Base.
    """
    prompt = f"""
    You are an expert Proposal Manager. Your task is to write the '{section_name}' section for a proposal in response to the following RFP.
    
    RFP Context:
    {rfp_text[:20000]}  # Truncate to avoid context limit if necessary
    
    Knowledge Base (Use this information to answer accurately):
    {knowledge_base_text[:50000]} # Truncate to avoid excessive token usage
    
    Section Requirements:
    {additional_instructions}
    
    Style Guide:
    - Professional, persuasive, and concise.
    - Use clear headings and bullet points where appropriate.
    - PRIORITIZE information from the Knowledge Base if relevant (e.g., Company History, Case Studies).
    - TONE/PERSONA: {persona}
    
    Output:
    Write ONLY the content for the '{section_name}' section. Do not include introductory text like "Here is the section...".
    """
    return get_gemini_response(prompt)

def generate_full_offer_plan(rfp_text):
    """
    Generates a plan or skeleton for the offer.
    """
    # This could be used to generate the structure dynamically if needed.
    # For now, we stick to the predefined structure in the requirements.
    pass
