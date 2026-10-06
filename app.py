import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NeuraForge AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CHECK API KEY
# ============================================================

if not GEMINI_API_KEY:

    st.error(
        """
        ❌ GEMINI_API_KEY not found.

        Create a `.env` file in your project folder:

        GEMINI_API_KEY=YOUR_API_KEY
        GEMINI_MODEL=gemini-3.5-flash-lite
        """
    )

    st.stop()


# ============================================================
# GEMINI CLIENT
# ============================================================

try:

    client = genai.Client(
        api_key=GEMINI_API_KEY,
        http_options=types.HttpOptions(
            timeout=30000
        )
    )

except Exception as e:

    st.error(
        f"❌ Could not initialize Gemini:\n\n{e}"
    )

    st.stop()


# ============================================================
# PAGE STYLE
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        margin-top: 10px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    .footer {
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        font-size: 14px;
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
    """
    <div class="subtitle">
    Transform your ideas into complete AI-powered project blueprints
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Project Configuration")

    selected_model = st.selectbox(
        "🤖 Gemini Model",
        [
            "gemini-3.5-flash-lite"
        ]
    )

    domain = st.selectbox(
        "🌐 Project Domain",
        [
            "Artificial Intelligence",
            "Machine Learning",
            "Generative AI",
            "Computer Vision",
            "Natural Language Processing",
            "Data Science",
            "Cybersecurity",
            "Healthcare",
            "Education",
            "Finance",
            "Agriculture",
            "Environment",
            "Other"
        ]
    )

    difficulty = st.selectbox(
        "📊 Difficulty Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    st.markdown("---")

    st.info(
        """
        **NeuraForge AI**

        Generate:

        • Project Overview
        • Problem Statement
        • Objectives
        • Features
        • Technology Stack
        • AI/ML Component
        • Architecture
        • Database
        • APIs
        • Folder Structure
        • Roadmap
        • Testing
        • Future Enhancements
        • Resume Description
        """
    )


# ============================================================
# PROJECT IDEA
# ============================================================

st.markdown(
    '<div class="section-title">'
    '💡 Describe Your Project Idea'
    '</div>',
    unsafe_allow_html=True
)

project_idea = st.text_area(
    "Project Idea",
    placeholder=(
        "Example:\n"
        "I want to build an AI-based system that detects "
        "online scams and phishing messages."
    ),
    height=180
)


# ============================================================
# ADDITIONAL DETAILS
# ============================================================

col1, col2 = st.columns(2)


with col1:

    preferred_technologies = st.text_input(
        "🛠️ Preferred Technologies",
        placeholder="Example: Python, Streamlit, MongoDB"
    )


with col2:

    target_users = st.text_input(
        "👥 Target Users",
        placeholder="Example: Students, organizations"
    )


# ============================================================
# CREATE PROMPT
# ============================================================

def create_project_prompt():

    technologies = (
        preferred_technologies.strip()
        if preferred_technologies.strip()
        else "Choose suitable modern technologies."
    )

    users = (
        target_users.strip()
        if target_users.strip()
        else "Identify suitable target users."
    )

    return f"""
You are NeuraForge AI, an expert AI project architect.

Create a practical and implementable project blueprint.

PROJECT IDEA:
{project_idea}

DOMAIN:
{domain}

DIFFICULTY:
{difficulty}

PREFERRED TECHNOLOGIES:
{technologies}

TARGET USERS:
{users}


Generate these sections:

# 1. Project Title

# 2. Project Overview

# 3. Problem Statement

# 4. Objectives

# 5. Target Users

# 6. Key Features

# 7. Technology Stack

Include:
- Frontend
- Backend
- AI/ML
- Database
- APIs
- Deployment

# 8. AI/ML Component

Explain the AI model, input,
processing and output.

# 9. System Architecture

Explain:

User
↓
Frontend
↓
Backend
↓
AI/ML
↓
Database
↓
Response

# 10. Database Design

Provide tables/collections
and important fields.

# 11. API Design

Provide important API endpoints
with HTTP methods and purposes.

# 12. Project Folder Structure

Provide a professional folder structure.

# 13. Development Roadmap

Give a step-by-step development plan.

# 14. Possible Challenges

List challenges and solutions.

# 15. Testing Strategy

Include unit, integration,
API, UI and security testing.

# 16. Future Enhancements

Give at least 6 useful enhancements.

# 17. Resume Description

Give:
- 2-3 line resume description
- 3-5 ATS-friendly bullet points

IMPORTANT:

Make the project realistic for a student.

Use Markdown.

Keep the explanation detailed but concise.

Avoid unnecessary repetition.
"""


# ============================================================
# GEMINI GENERATION
# ============================================================

def generate_with_gemini(prompt, model):

    try:

        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    thinking_level="low"
                ),
                temperature=0.7
            )
        )

        if response.text:

            return response.text

        return None


    except Exception as e:

        error = str(e)


        # ----------------------------------------------------
        # TIMEOUT
        # ----------------------------------------------------

        if (
            "timeout" in error.lower()
            or "timed out" in error.lower()
        ):

            st.error(
                """
                ⏱️ Gemini took too long to respond.

                Please try again with a shorter project idea.
                """
            )

            return None


        # ----------------------------------------------------
        # 503
        # ----------------------------------------------------

        if (
            "503" in error
            or "UNAVAILABLE" in error
            or "high demand" in error.lower()
        ):

            st.error(
                """
                ⚠️ Gemini is currently experiencing
                high demand.

                Please wait a little and try again.
                """
            )

            return None


        # ----------------------------------------------------
        # 429
        # ----------------------------------------------------

        if (
            "429" in error
            or "RESOURCE_EXHAUSTED" in error
        ):

            st.error(
                """
                ⚠️ Gemini API rate limit reached.

                Please wait and try again.
                """
            )

            return None


        # ----------------------------------------------------
        # AUTHENTICATION
        # ----------------------------------------------------

        if (
            "401" in error
            or "403" in error
            or "API key" in error
        ):

            st.error(
                """
                ❌ Gemini authentication failed.

                Check your GEMINI_API_KEY in `.env`.
                """
            )

            return None


        # ----------------------------------------------------
        # OTHER ERROR
        # ----------------------------------------------------

        st.error(
            f"""
            ❌ Gemini Error:

            {error}
            """
        )

        return None


# ============================================================
# GENERATE BUTTON
# ============================================================

st.markdown("---")

generate_button = st.button(
    "🚀 Generate Project Blueprint",
    type="primary",
    use_container_width=True
)


# ============================================================
# GENERATE
# ============================================================

if generate_button:

    if not project_idea.strip():

        st.warning(
            "⚠️ Please enter your project idea first."
        )

    else:

        prompt = create_project_prompt()

        with st.spinner(
            "🧠 NeuraForge AI is generating your blueprint..."
        ):

            blueprint = generate_with_gemini(
                prompt,
                selected_model
            )


        if blueprint:

            st.session_state["blueprint"] = blueprint

            st.success(
                "✅ Project blueprint generated successfully!"
            )


# ============================================================
# DISPLAY RESULT
# ============================================================

if "blueprint" in st.session_state:

    st.markdown("---")

    st.markdown(
        '<div class="section-title">'
        '📋 Generated Project Blueprint'
        '</div>',
        unsafe_allow_html=True
    )

    blueprint = st.session_state["blueprint"]

    st.markdown(blueprint)

    st.markdown("---")

    st.download_button(
        "📥 Download Project Blueprint",
        data=blueprint,
        file_name="NeuraForge_Project_Blueprint.txt",
        mime="text/plain",
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

    🧠 <b>NeuraForge AI</b>

    <br><br>

    AI-Powered Project Blueprint Generator

    <br><br>

    Built with ❤️ using Streamlit + Google Gemini

    </div>
    """,
    unsafe_allow_html=True
)