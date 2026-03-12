import streamlit as st
import os
from src.parser import extract_text_from_pdf, extract_text_from_docx, extract_text_from_excel, load_knowledge_base
from src.generator import generate_section
from src.analyzer import perform_gap_analysis
from src.exporter import export_to_docx
from src.theme_manager import ThemeManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Theme Initialization
theme_manager = ThemeManager()
theme_manager.initialize_theme()

# Page Config
st.set_page_config(
    page_title="RFP Genie | Enterprise Edition",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Crystal Teal" look
if st.session_state.get('theme') == 'dark':
    bg_gradient = "radial-gradient(circle at top left, #0f172a 0%, #020617 50%, #0f172a 100%)"
    text_color = "#f8fafc"
    card_bg = "rgba(30, 41, 59, 0.7)"
    input_bg = "rgba(15, 23, 42, 0.8) !important"
    sidebar_bg = "rgba(15, 23, 42, 0.4)"
else:
    bg_gradient = "radial-gradient(circle at top left, #f0fdfa 0%, #ffffff 50%, #f7fee7 100%)"
    text_color = "#0f172a"
    card_bg = "rgba(255, 255, 255, 0.7)"
    input_bg = "rgba(255, 255, 255, 0.8) !important"
    sidebar_bg = "rgba(255, 255, 255, 0.4)"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Global Reset & Page Background */
    div.stApp {{
        background: {bg_gradient};
    }}

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: {text_color};
    }}

    /* Headers with Teal Gradient */
    h1, h2, h3 {{
        font-weight: 700;
        letter-spacing: -0.025em;
        background: linear-gradient(135deg, #0f766e, #059669); /* Teal-700 to Emerald-600 */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    h1 {{
        background: linear-gradient(135deg, #14b8a6, #84cc16); /* Teal to Lime */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
        padding-bottom: 0.5rem;
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }}

    /* Button Styling - Ocean Gradient */
    .stButton>button {{
        width: 100%;
        border-radius: 12px;
        height: 3.2em;
        background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%); /* Teal-500 to 600 */
        color: white;
        border: none;
        font-weight: 600;
        box-shadow: 0 4px 14px rgba(20, 184, 166, 0.3);
        transition: all 0.3s ease;
    }}

    /* Hover Effects */
    .stButton>button:hover {{
        background: linear-gradient(135deg, #2dd4bf 0%, #14b8a6 100%); /* Teal-400 */
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(20, 184, 166, 0.4);
    }}

    /* Cards - Glassmorphism */
    .stExpander {{
        border: 1px solid rgba(20, 184, 166, 0.1);
        border-radius: 16px;
        background: {card_bg};
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        margin-bottom: 1rem;
    }}
    .stExpander:hover {{
        border-color: #2dd4bf; /* Teal-400 */
        box-shadow: 0 10px 15px -3px rgba(20, 184, 166, 0.15);
    }}

    /* Inputs */
    input, textarea, .stSelectbox > div > div {{
        background-color: {input_bg};
        border: 1px solid #ccfbf1 !important; /* Teal-100 */
        border-radius: 10px !important;
        color: {text_color} !important;
    }}
    input:focus, textarea:focus {{
        background-color: transparent !important;
        border-color: #14b8a6 !important;
        box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.2) !important;
    }}

    /* Upload Zone */
    div[data-testid="stFileUploader"] {{
        background-color: rgba(240, 253, 250, 0.05);
        border: 2px dashed #99f6e4;
        border-radius: 16px;
        color: #14b8a6;
    }}

    /* Metric */
    div[data-testid="metric-container"] {{
        background: {card_bg};
        border: 1px solid #ccfbf1;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }}
</style>
""", unsafe_allow_html=True)
# Application Header
col1, col2, col3 = st.columns([1, 10, 1])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/8654/8654272.png", width=60) # Teal icon
with col2:
    st.title("Proposal Studio")
with col3:
    if st.session_state.get('theme') == 'light':
        if st.button("🌙", help="Switch to Dark Mode"):
            theme_manager.set_theme('dark')
            st.rerun()
    else:
        if st.button("☀️", help="Switch to Light Mode"):
            theme_manager.set_theme('light')
            st.rerun()
st.markdown("---")

# --- SIDEBAR: Global Context & Settings ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Daco_2.png/640px-Daco_2.png", width=50) # Placeholder generic logo idea or remove
    st.header("Engagement Context")
    
    # 1. API Configuration (Hidden if set)
    api_key_env = os.getenv("GOOGLE_API_KEY")
    if api_key_env:
        st.caption("✅ Gemini API Active")
    else:
        api_key_input = st.text_input("API Key", type="password")
        if api_key_input:
            os.environ["GOOGLE_API_KEY"] = api_key_input
            import google.generativeai as genai
            genai.configure(api_key=api_key_input)
    
    st.divider()
    
    # 2. Knowledge Base (Global Context)
    st.subheader("📚 Knowledge Assets")
    kb_path = "knowledge_base"
    if not os.path.exists(kb_path):
        os.makedirs(kb_path)
    
    # Simple File count
    kb_files = os.listdir(kb_path)
    st.metric("Active Documents", len(kb_files))
    
    with st.expander("Manage Assets"):
        uploaded_kb_files = st.file_uploader("Add 'Golden Docs'", type=['pdf', 'docx', 'xlsx'], accept_multiple_files=True)
        if uploaded_kb_files:
            for uf in uploaded_kb_files:
                with open(os.path.join(kb_path, uf.name), "wb") as f:
                    f.write(uf.getbuffer())
            st.rerun()
            
        if st.button("Reload Context Memory"):
            with st.spinner("Indexing assets..."):
                kb_text = load_knowledge_base(kb_path)
                st.session_state['kb_text'] = kb_text
            st.success("Context Updated")

    if 'kb_text' not in st.session_state:
        st.session_state['kb_text'] = ""

    st.divider()

    # 3. Persona (Tone of Voice)
    st.subheader("🎙️ Voice & Tone")
    persona_options = [
        "Standard (Professional, Balanced)",
        "Strategy Consultant (High-level, Insightful)",
        "Sales Executive (Persuasive, Value-focused)",
        "Technical Architect (Precise, Detailed)",
        "Legal Counsel (Formal, Risk-averse)"
    ]
    if 'persona' not in st.session_state:
        st.session_state['persona'] = persona_options[0]
        
    st.session_state['persona'] = st.selectbox("Select Persona", persona_options, index=persona_options.index(st.session_state['persona']) if st.session_state['persona'] in persona_options else 0)

# --- MAIN WORKFLOW ---

# 1. Document Upload (The Trigger)
col_upload, col_status = st.columns([2, 1])
if 'rfp_text' not in st.session_state:
    st.session_state['rfp_text'] = None
if 'offer_sections' not in st.session_state:
    st.session_state['offer_sections'] = {}

with col_upload:
    uploaded_file = st.file_uploader("Step 1: Upload Request for Proposal (RFP)", type=['pdf', 'docx', 'xlsx'], help="Supports PDF, Word, and Excel formats.")

with col_status:
    if uploaded_file:
        if st.button("Analyze & Parse Document"):
            with st.spinner("Deconstructing document structure..."):
                if uploaded_file.name.endswith('.pdf'):
                    text = extract_text_from_pdf(uploaded_file)
                elif uploaded_file.name.endswith('.docx'):
                    text = extract_text_from_docx(uploaded_file)
                elif uploaded_file.name.endswith('.xlsx'):
                    text = extract_text_from_excel(uploaded_file)
                else:
                    text = None
                
                if text:
                    st.session_state['rfp_text'] = text
                    st.success("Document Successfully Parsed")
                else:
                    st.error("Parsing Failed")

if st.session_state['rfp_text']:
    st.divider()
    
    # 2. Tabs for Workflow
    tab_draft, tab_analyze, tab_refine = st.tabs(["2. Draft Proposal", "3. Strategic Gap Analysis", "4. Refinement"])
    
    SECTIONS = [
        "Executive Summary",
        "Strategic Value Proposition (Why Us)",
        "Scope of Work & Methodology",
        "Delivery Model & Timeline",
        "Governance & Risk Management",
        "Technical Solution Architecture",
        "Commercials & Pricing Model",
        "Case Studies & Capabilities",
        "Team Profiles",
        "Appendix"
    ]

    with tab_draft:
        col_d1, col_d2 = st.columns([1, 3])
        with col_d1:
            st.markdown("#### Configuration")
            selected_sections = st.multiselect("Select Modules", SECTIONS, default=[SECTIONS[0], SECTIONS[1], SECTIONS[2]])
            st.caption(f"Generating with **{st.session_state['persona']}** voice.")
            
            if st.button("🚀 Initiating Drafting Engine"):
                progress_bar = st.progress(0)
                for idx, section in enumerate(selected_sections):
                    with st.spinner(f"Drafting {section}..."):
                        content = generate_section(
                            st.session_state['rfp_text'], 
                            section, 
                            knowledge_base_text=st.session_state.get('kb_text', ""),
                            persona=st.session_state['persona']
                        )
                        st.session_state['offer_sections'][section] = content
                    progress_bar.progress((idx + 1) / len(selected_sections))
                st.success("Drafting Complete")
            
            if st.session_state.get('offer_sections'):
                st.markdown("---")
                docx_file = export_to_docx(st.session_state['offer_sections'])
                st.download_button(
                    label="📥 Export Final Proposal (.docx)",
                    data=docx_file,
                    file_name="Consulting_Proposal_Draft.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

        with col_d2:
            st.markdown("#### Live Preview")
            if st.session_state.get('offer_sections'):
                for section in SECTIONS:
                    if section in st.session_state['offer_sections']:
                        with st.expander(section, expanded=False):
                            st.markdown(st.session_state['offer_sections'][section])
            else:
                st.info("Select modules and click 'Initiate Drafting Engine' to begin.")

    with tab_analyze:
        st.markdown("#### Compliance & Risk Assessment")
        if st.session_state.get('offer_sections'):
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                if st.button("Run Strategic Gap Analysis"):
                    with st.spinner("Analyzing competitive position..."):
                        full_offer_text = "\n\n".join([f"## {k}\n{v}" for k, v in st.session_state['offer_sections'].items()])
                        analysis_result = perform_gap_analysis(st.session_state['rfp_text'], full_offer_text)
                        st.session_state['gap_analysis'] = analysis_result
            
            with col_a2:
                if st.button("Run Detailed Compliance Shredding"):
                    with st.spinner("Auditing line-item requirements..."):
                        from src.analyzer import shred_requirements_and_grade
                        full_offer_text = "\n\n".join([f"## {k}\n{v}" for k, v in st.session_state['offer_sections'].items()])
                        df = shred_requirements_and_grade(st.session_state['rfp_text'], full_offer_text)
                        st.session_state['shred_analysis'] = df

            if 'gap_analysis' in st.session_state:
                st.markdown("##### Executive Summary of Gaps")
                st.markdown(st.session_state['gap_analysis'])
            
            if 'shred_analysis' in st.session_state:
                st.markdown("---")
                st.markdown("##### Detailed Requirement Traceability Matrix (RTM)")
                st.dataframe(
                    st.session_state['shred_analysis'], 
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Score": st.column_config.ProgressColumn(
                            "Compliance Score",
                            format="%d%%",
                            min_value=0,
                            max_value=100,
                        ),
                    }
                )
        else:
            st.info("Draft proposal first to run analysis.")

    with tab_refine:
        st.markdown("#### Iterative Refinement")
        if st.session_state.get('offer_sections'):
            section_to_edit = st.selectbox("Select Module to Refine", list(st.session_state['offer_sections'].keys()))
            col_r1, col_r2 = st.columns([1, 1])
            
            with col_r1:
                st.markdown("**Current Content**")
                st.caption("Review the generated content below.")
                st.markdown(st.session_state['offer_sections'][section_to_edit])
                
            with col_r2:
                st.markdown("**Refinement Instructions**")
                new_instructions = st.text_area("Enter feedback for the AI", placeholder="e.g., 'Make the tone more aggressive' or 'Include our ISO 27001 certification details'.")
                if st.button("Apply Adjustments"):
                    with st.spinner(f"Refining {section_to_edit}..."):
                        updated_content = generate_section(
                            st.session_state['rfp_text'], 
                            section_to_edit, 
                            additional_instructions=new_instructions,
                            knowledge_base_text=st.session_state.get('kb_text', ""),
                            persona=st.session_state['persona']
                        )
                        st.session_state['offer_sections'][section_to_edit] = updated_content
                        st.success("Module Updated")
                        st.rerun()
        else:
            st.info("No content to edit yet.")

else:
    st.info("👆 Please upload an RFP document to begin the engagement.")

