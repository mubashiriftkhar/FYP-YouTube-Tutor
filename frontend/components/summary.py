
import streamlit as st
import asyncio
from Backend.SummarizerAgent import Summarizer
from Backend.state import State


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

def summary_ui(state: State):
    print(state)
    st.markdown("<div class='section-title'>Video Summary</div>", unsafe_allow_html=True)

    if st.button("Generate Summary"):

        st.markdown("### 📄 Summary")

        # Chat-style assistant container
        with st.chat_message("assistant"):

            placeholder = st.empty()
            full_text = ""

            # 🔵 Bubble loading animation
            import time
            loading_placeholder = st.empty()

            def bubble_loader():
                dots = ["⏳", "⏳.", "⏳..", "⏳..."]
                for i in range(100):  # runs until replaced
                    loading_placeholder.markdown(f"**Generating summary {dots[i % 4]}**")
                    time.sleep(0.3)

            # Start loader
            import threading
            stop_loading = False

            def run_loader():
                while not stop_loading:
                    bubble_loader()

            loader_thread = threading.Thread(target=run_loader)
            loader_thread.start()

            # 🔥 REAL STREAM
            def real_stream():
                async_gen = Summarizer(state=state)
                yield from stream_async_generator(async_gen)

            first_token_received = False

            for token in real_stream():

                # Stop loader on first token
                if not first_token_received:
                    stop_loading = True
                    loading_placeholder.empty()
                    first_token_received = True

                full_text += token
                placeholder.markdown(full_text)

            # Ensure loader stops
            stop_loading = True
            loading_placeholder.empty()