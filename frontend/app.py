import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(ROOT_DIR)
import streamlit as st
from utils.styles import apply_styles
from components.chat import chat_ui
from components.summary import summary_ui
from components.quiz import quiz_ui

st.set_page_config(page_title="AI YouTube Tutor", layout="wide")

apply_styles()

# -------------------- GLOBAL STATE (FIXED) --------------------
if "app_state" not in st.session_state:
    st.session_state.app_state = {
        "link": "",
        "query": "",
        "vedioTitle": "",
        "TitledQuery": "",
        "isEnglishAvailable": True,
        "EnglishTranscript": "",
        "SimilaritySearchResults": [],
        "KeywordSearchResults": [],
        "MergeResults": [],
        "chunks": [],
        "embeddings": [],
        "rerankedDocuments": [],
    }

# reference
state = st.session_state.app_state


# -------------------- HEADER --------------------
st.markdown(
    "<h1 style='text-align:center;color:#FF0000;'>🎥 AI YouTube Tutor</h1>",
    unsafe_allow_html=True
)

# -------------------- SECTION TOGGLE --------------------
section = st.radio(
    "",
    ["💬 Chatbot", "📄 Summary", "🧠 Quiz"],
    horizontal=True
)

st.markdown("<div class='fade-in'>", unsafe_allow_html=True)


# -------------------- ROUTING --------------------
if section == "💬 Chatbot":
    # st.write("### Debug State (Chat)")
    # st.json(state)  # better than print

    chat_ui(state=state)

elif section == "📄 Summary":
    # st.write("### Debug State (Summary)")
    # st.json(state)

    summary_ui(state=state)

elif section == "🧠 Quiz":
    # st.write("### Debug State (Quiz)")
    # st.json(state)

    quiz_ui(state=state)


st.markdown("</div>", unsafe_allow_html=True)