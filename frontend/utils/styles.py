def apply_styles():
    import streamlit as st

    st.markdown("""
    <style>
    /* Background */
    .stApp {
        background-color: #0f0f0f;
        color: white;
    }

    /* Buttons */
    .stButton>button {
        background-color: #FF0000;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #cc0000;
        transform: scale(1.05);
    }

    /* Input */
    .stTextInput>div>div>input {
        background-color: #1c1c1c;
        color: white;
        border-radius: 10px;
    }

    /* Section Header */
    .section-title {
        font-size: 28px;
        font-weight: bold;
        color: #FF0000;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Smooth fade animation */
    .fade-in {
        animation: fadeIn 1s ease-in;
    }

    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    </style>
    """, unsafe_allow_html=True)