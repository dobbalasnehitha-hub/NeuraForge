
import os
import requests
import streamlit as st
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434"
)

DEFAULT_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="NeuraForge AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #777777;
        margin-bottom: 35px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 700;
    }

    .stButton > button {
        width: 100%;
        font-weight: 600;
        border-radius: 10px;
        padding: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🧠 NeuraForge AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Transform your raw project idea into a complete AI-powered project blueprint'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ NeuraForge Settings")

    model = st.text_input(
        "Ollama Model",
        value=DEFAULT_MODEL
    )

    st.divider()

    st.subheader("🎯 Project Settings")

    domain = st.selectbox(
        "Project Domain",
        [
            "Artificial Intelligence",
            "Machine Learning",
            "Generative AI",
            "Web Development",
            "Data Science",
            "Cybersecurity",
            "Healthcare",
            "Education",
            "Environment",
            "Other"
        ]
    )

    difficulty = st.selectbox(
        "Project Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    st.divider()

    st.info(
        "NeuraForge AI uses a local Ollama model. "
        "Your project idea is processed locally."
    )


# ============================================================
# PROJECT IDEA INPUT
# ============================================================

st.markdown(
    '<div class="section-title">🚀 Describe Your Project Idea</div>',
    unsafe_allow_html=True
)

st.write(
    "Enter a simple idea. NeuraForge will transform it into "
    "a structured project blueprint."
)

project_idea = st.text_area(
    "Project Idea",
    placeholder=(
        "Example: I want to build an AI system that predicts "
        "flood risk using rainfall and river data."
    ),
    height=160
)


# ============================================================
# ADDITIONAL REQUIREMENTS
# ============================================================

st.markdown("### 🛠️ Additional Requirements")

col1, col2 = st.columns(2)

with col1:

    preferred_technologies = st.text_input(
        "Preferred Technologies",
        placeholder="Example: Python, Streamlit, FastAPI"
    )

with col2:

    target_users = st.text_input(
        "Target Users",
        placeholder="Example: Students, researchers, farmers"
    )


# ============================================================
# GENERATE BUTTON
# ============================================================

st.markdown("")

generate_button = st.button(
    "✨ Generate Project Blueprint"
)


# ============================================================
# OLLAMA FUNCTION
# ============================================================

def generate_with_ollama(prompt, selected_model):

    url = f"{OLLAMA_HOST}/api/chat"

    payload = {
        "model": selected_model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    response = requests.post(
        url,
        json=payload,
        timeout=180
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]


# ============================================================
# GENERATE BLUEPRINT
# ============================================================

if generate_button:

    if not project_idea.strip():

        st.warning(
            "⚠️ Please enter your project idea first."
        )

    else:

        prompt = f"""
You are NeuraForge AI, an expert AI project architect,
software engineer, and technical mentor.

Your job is to transform a student's raw project idea
into a practical and technically strong project blueprint.

PROJECT IDEA:
{project_idea}

PROJECT DOMAIN:
{domain}

PROJECT DIFFICULTY:
{difficulty}

PREFERRED TECHNOLOGIES:
{preferred_technologies if preferred_technologies else "Choose suitable technologies."}

TARGET USERS:
{target_users if target_users else "Determine suitable target users."}

Generate the project blueprint using the following structure.

# 1. PROJECT TITLE

Give a professional and unique project title.

# 2. PROJECT OVERVIEW

Explain the project clearly in simple but professional language.

# 3. PROBLEM STATEMENT

Explain the real-world problem being solved.

# 4. OBJECTIVES

Give 5 to 8 clear objectives.

# 5. TARGET USERS

Explain who will use the system.

# 6. KEY FEATURES

Give the major features of the application.

# 7. TECHNOLOGY STACK

Recommend:
- Frontend
- Backend
- Database
- AI/ML
- APIs
- Deployment
- Other required technologies

# 8. AI/ML COMPONENT

Explain:
- Which AI model or approach should be used
- Why it is suitable
- Input
- Processing
- Output

# 9. SYSTEM ARCHITECTURE

Explain the complete flow:

User
→ Frontend
→ Backend
→ AI/ML
→ Database
→ Response

Give a detailed architecture explanation.

# 10. DATABASE DESIGN

Suggest the required database tables/collections
and important fields.

# 11. API DESIGN

Suggest important API endpoints if APIs are required.

# 12. PROJECT FOLDER STRUCTURE

Provide a clean and realistic folder structure.

# 13. DEVELOPMENT ROADMAP

Divide development into practical phases.

Example:

Phase 1 - Setup
Phase 2 - Backend
Phase 3 - AI
Phase 4 - Database
Phase 5 - Frontend
Phase 6 - Testing
Phase 7 - Deployment

# 14. POSSIBLE CHALLENGES

List technical challenges and how to solve them.

# 15. TESTING STRATEGY

Explain how the application should be tested.

# 16. FUTURE ENHANCEMENTS

Give 5 to 8 realistic future improvements.

# 17. RESUME DESCRIPTION

Write 3 strong resume bullet points describing this project.

IMPORTANT:

Make the project realistic for a college student.

Avoid unnecessarily complex technologies.

Prefer open-source and locally runnable technologies where possible.

Give practical implementation suggestions rather than generic statements.
"""

        # ====================================================
        # AI GENERATION
        # ====================================================

        with st.spinner(
            "🧠 NeuraForge is designing your project..."
        ):

            try:

                result = generate_with_ollama(
                    prompt,
                    model
                )

                st.success(
                    "✅ Project blueprint generated successfully!"
                )

                # ============================================
                # RESULTS
                # ============================================

                st.markdown("---")

                st.markdown(
                    "## 📋 Your Project Blueprint"
                )

                st.markdown(result)

                # ============================================
                # DOWNLOAD
                # ============================================

                st.markdown("---")

                st.download_button(
                    label="📥 Download Blueprint",
                    data=result,
                    file_name="neuraforge_project_blueprint.txt",
                    mime="text/plain"
                )

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Could not connect to Ollama."
                )

                st.info(
                    "Make sure Ollama is installed and running."
                )

                st.code(
                    "ollama list"
                )

            except requests.exceptions.Timeout:

                st.error(
                    "⏱️ Ollama took too long to respond."
                )

                st.info(
                    "Try a smaller/faster model or wait a little longer."
                )

            except requests.exceptions.HTTPError as error:

                st.error(
                    "❌ Ollama returned an HTTP error."
                )

                st.code(
                    str(error)
                )

            except KeyError:

                st.error(
                    "❌ Unexpected response received from Ollama."
                )

            except Exception as error:

                st.error(
                    "❌ Something went wrong."
                )

                st.code(
                    str(error)
                )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "NeuraForge AI • AI-Powered Project Architecture Platform"
)
