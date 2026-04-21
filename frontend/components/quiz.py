import streamlit as st
from Backend.state import State
from Backend.quize import QuizGenerator


def quiz_ui(state: State):
    st.markdown("<div class='section-title'>Quiz</div>", unsafe_allow_html=True)

    # ---------------- SESSION STATE INIT ----------------
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = []

    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}

    # ---------------- GENERATE QUIZ ----------------
    if st.button("Generate Quiz"):

        if state["link"] == "":
            st.warning("Link not provided")
            return

        with st.spinner("Generating Quiz..."):
            st.session_state.quiz_data = QuizGenerator(state=state)

        st.session_state.user_answers = {}
        st.rerun()

    quiz_data = st.session_state.quiz_data
    user_answers = st.session_state.user_answers

    # ---------------- SHOW QUIZ ----------------
    if quiz_data:

        for i, q in enumerate(quiz_data):

            # Extract question + tuple
            question = list(q.keys())[0]
            options, opt2, opt3, opt4, correct, explanation = q[question]

            st.markdown(f"### {i+1}. {question}")

            selected = st.radio(
                "Select an option:",
                ["-- Select an answer --", options, opt2, opt3, opt4],
                key=f"q_{i}_{question}"
            )

            if selected != "-- Select an answer --":
                user_answers[question] = selected

        st.session_state.user_answers = user_answers

        # ---------------- CHECK ANSWERS ----------------
        if st.button("Check Answers"):

            st.markdown("## ✅ Results")

            score = 0

            for i, q in enumerate(quiz_data):

                question = list(q.keys())[0]
                options, opt2, opt3, opt4, correct, explanation = q[question]

                user_ans = user_answers.get(question)

                if user_ans == correct:
                    st.success(f"✔ {question}")
                    score += 1
                else:
                    st.error(f"✘ {question}")
                    st.write(f"Correct Answer: **{correct}**")

                st.info(f"Explanation: {explanation}")

            st.markdown(f"## 🎯 Final Score: {score}/{len(quiz_data)}")