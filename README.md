# Proposal Studio (RFP Genie Enterprise Edition) 🧞‍♂️✨

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Gemini](https://img.shields.io/badge/AI-Google_Gemini-orange)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**Proposal Studio** (internally known as RFP Genie) is an enterprise-grade, AI-powered toolkit designed to automate, analyze, and refine the Request for Proposal (RFP) response process. Powered by Google's Gemini LLM, this platform ingests complex RFP documents and generates targeted, high-quality consulting proposals with extreme speed.

---

## 🚀 Features

- **Intelligent Document Ingestion**: Seamlessly extracts and structures text from `.pdf`, `.docx`, and `.xlsx` RFP files.
- **Dynamic Drafting Engine**: Automatically generates core proposal modules including Executive Summaries, Strategic Value Propositions, Delivery Models, Pricing, and more.
- **Strategic Gap Analysis**: Automatically assesses the generated proposal against the original RFP to identify compliance gaps, risks, and missing elements.
- **Detailed Requirement Traceability**: Shreds the RFP into granular line items and scores the proposal's compliance percentage for each requirement.
- **Iterative Refinement**: Refine generated modules interactively. Apply specific feedback ("Make the tone more aggressive", "Include ISO 27001 details") to perfect the output.
- **Global Knowledge Base Integration**: Upload "Golden Docs" (past winning proposals, case studies, company profiles) for the AI to dynamically reference while drafting.
- **Customizable Personas**: Choose how the AI writes—from a 'Strategy Consultant' to a 'Technical Architect' to 'Legal Counsel'.
- **Modern UI/UX**: Features an elegant "Crystal Teal" glassmorphism interface with built-in Light/Dark mode.
- **One-Click Export**: Export the finalized, combined proposal directly to a `.docx` file.

---

## 🛠️ Tech Stack

- **Frontend / Framework**: [Streamlit](https://streamlit.io/)
- **Core AI**: Google [Generative AI (Gemini)](https://ai.google.dev/)
- **Document Parsing**: `PyPDF2`, `python-docx`, `pandas`, `openpyxl`
- **Styling**: Custom CSS with Glassmorphism and responsive layouts.

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/proposal-studio.git
   cd proposal-studio
   ```

2. **Set up a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   Ensure you have a `requirements.txt` file (if not, pip install the necessary packages).
   ```bash
   pip install -r requirements.txt
   ```
   *(Core requirements usually include: `streamlit`, `google-generativeai`, `python-dotenv`, `PyPDF2`, `python-docx`, `pandas`, `openpyxl`)*

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your Google Gemini API Key:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```
   *Alternatively, you can securely input your API key directly into the app's sidebar when it's running.*

5. **Run the Application:**
   ```bash
   streamlit run main.py
   ```

---

## 📖 How to Use

1. **Context & Setup (Sidebar)**: 
   - Verify your Gemini API key is loaded.
   - Upload your company's "Golden Docs" to the Knowledge Base.
   - Select your desired "Voice & Tone" persona.
2. **Step 1: Upload RFP**: 
   - Drag and drop your client's Request for Proposal (PDF, DOCX, XLSX) into the main upload zone and click "Analyze & Parse Document".
3. **Step 2: Draft Proposal**: 
   - In the "Draft Proposal" tab, select the specific modules you need generated.
   - Click "Initiate Drafting Engine". Preview the results live or export immediately to `.docx`.
4. **Step 3: Strategic Gap Analysis**: 
   - Run the Gap Analysis or Detailed Compliance Shredding to see how well your generated proposal answers the client's specific demands.
5. **Step 4: Refinement**: 
   - Navigate to the "Iterative Refinement" tab, select a module, and provide specific prompt feedback for the AI to rewrite or adjust the content.

---

## 📁 Project Structure

```text
├── main.py                  # Streamlit frontend and core application logic
├── src/
│   ├── parser.py            # Logic for extracting text from PDFs, DOCXs, and loading KB
│   ├── generator.py         # Prompts and LLM interaction for drafting sections
│   ├── analyzer.py          # Gap analysis and requirement shredding algorithms
│   ├── exporter.py          # Docx compilation and export logic
│   └── theme_manager.py     # UI Theme handling functionality
├── knowledge_base/          # Directory holding reference "Golden Docs"
├── .env                     # Local environment variables (Do NOT commit)
├── .gitignore               # Ignored files for security
└── README.md                # This file
```

---

## 🔒 Security Note

This repository contains a `.gitignore` specifically designed to exclude the `.env` file and the `/knowledge_base/` folder. **Do not commit sensitive API keys or proprietary company documents to public repositories.** Always use environment variables or Streamlit's Secrets management for deployments.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/proposal-studio/issues).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
