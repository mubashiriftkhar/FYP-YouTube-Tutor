
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(ROOT_DIR)
import streamlit as st
from Backend.orchestrator import orchestrator
from Backend.GetAnswer import results
from Backend.state import State
import asyncio



def stream_async_generator(async_gen):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def get_next(gen):
        try:
            return await gen.__anext__(), False
        except StopAsyncIteration:
            return None, True

    while True:
        chunk, done = loop.run_until_complete(get_next(async_gen))
        if done:
            break
        yield chunk
def stream_text(generator):
    """Utility to stream tokens"""
    placeholder = st.empty()
    full_text = ""

    for token in generator:
        full_text += token
        placeholder.markdown(full_text)
    
    return full_text

orch=orchestrator()

def chat_ui(state:State):

    st.markdown("<div class='section-title'>Chat with YouTube Video</div>", unsafe_allow_html=True)

    # -------- SESSION STATE --------
    if "chat_ready" not in st.session_state:
        st.session_state.chat_ready = False

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "video_title" not in st.session_state:
        st.session_state.video_title = ""

    # -------- URL INPUT --------
    url = st.text_input("🔗 Enter YouTube URL")

    # -------- LOAD VIDEO --------
    if st.button("Load Video"):
        if not url:
            st.warning("Please enter a URL")
            return

        state["link"] = url

        with st.spinner("Processing video... ⏳"):
            orch.pipeline_1_execute(state=state)

        # Save title
        st.session_state.video_title = state.get("vedioTitle", "Unknown Title")
        st.session_state.chat_ready = True

        st.success("✅ Video processed!")

    # -------- SHOW VIDEO TITLE --------
    if st.session_state.chat_ready:
        st.markdown(f"### 🎬 {st.session_state.video_title}")

    # -------- CHAT UI --------
    if st.session_state.chat_ready:

        # Display chat history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Chat input (REAL chatbot input)
        user_query = st.chat_input("Ask something about the video...")

        if user_query:
            # Save user message
            st.session_state.messages.append({
                "role": "user",
                "content": user_query
            })

            # Show user message immediately
            with st.chat_message("user"):
                st.markdown(user_query)

            # Update state
            state["query"] = user_query

            # Run retrieval BEFORE streaming
            orch.pipline_2_execute(state=state)
            print(state)
            
            # Assistant response
            with st.chat_message("assistant"):
                placeholder = st.empty()
                full_text = ""

                def real_stream():
                    async_gen = results(state=state)
                    yield from stream_async_generator(async_gen)

                # STREAM TOKENS
                for token in real_stream():
                    full_text += token
                    placeholder.markdown(full_text)

            # Save assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_text
            })