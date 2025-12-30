import textwrap
import pandas as pd
import json
from src.generator import get_gemini_response

def perform_gap_analysis(rfp_text, offer_text):
    """
    Analyzes the gap between RFP requirements and the proposed Offer.
    """
    prompt = f"""
    You are a deeply analytical Bid Manager. Perform a gap analysis between the RFP requirements and the proposed Offer.
    
    RFP Extract:
    {rfp_text[:15000]}
    
    Offer Extract:
    {offer_text[:15000]}
    
    Task:
    Compare the documents across the following 9 components:
    1. Scope
    2. Deliverables
    3. Timeline
    4. Pricing
    5. Technical Requirements
    6. Legal Terms
    7. QA
    8. Compliance
    9. Support
    
    Output Format:
    Return the result as a Markdown table with the following columns:
    | Component | RFP Requirement Summary | Our Offer Status | Gap/Risk Analysis |
    
    Highlight critical gaps in **Bold**.
    If a component is missing in the RFP or Offer, state "Not Found".
    """
    return get_gemini_response(prompt)

def shred_requirements_and_grade(rfp_text, offer_text):
    """
    Extracts individual requirements from RFP and grades the Offer against them.
    Returns a pandas DataFrame.
    """
    prompt = f"""
    You are a strict Compliance Officer. Your goal is to "shred" a technical RFP into individual line-item requirements and grade our response.
    
    RFP Content:
    {rfp_text[:20000]}
    
    Offer Content:
    {offer_text[:20000]}
    
    Task:
    1. Identify up to 20 KEY technical or functional requirements from the RFP.
    2. Check if the Offer addresses them.
    3. Assign a coverage score (0 = Not Addressed, 50 = Partially Addressed, 100 = Fully Compliant).
    
    Output Format:
    Return ONLY a raw JSON list of objects (no markdown blocks, no 'json' tag). Format:
    [
        {{
            "Requirement": "Must support SSO via SAML 2.0",
            "Offer_Response": "We propose Auth0 for identity management",
            "Score": 0,
            "Gap_Note": "Offer mentions Auth0 generally but does not explicitly confirm SAML 2.0 support."
        }},
        ...
    ]
    """
    response = get_gemini_response(prompt)
    
    # Cleaning response to ensure it's valid JSON
    clean_json = response.replace('```json', '').replace('```', '').strip()
    
    try:
        data = json.loads(clean_json)
        return pd.DataFrame(data)
    except Exception as e:
        # Fallback empty DF or error details
        return pd.DataFrame({"Error": [f"Failed to parse analysis: {str(e)}"], "Raw Output": [clean_json]})
