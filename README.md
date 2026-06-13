import streamlit as st
from main import get_sql_query_from_user_input
from streamlit_mic_recorder import mic_recorder
import whisper
import tempfile
import os


# -----------------------------
# Load Whisper Model
# -----------------------------
@st.cache_resource
def load_whisper():
    return whisper.load_model("base")


model = load_whisper()


# -----------------------------
# Session State
# -----------------------------
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

if "result" not in st.session_state:
    st.session_state.result = ""


# -----------------------------
# Speech To Text
# -----------------------------
def speech_to_text(audio):

    audio_bytes = audio.get("bytes")

    if not audio_bytes:
        return ""

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as tmp:

        tmp.write(audio_bytes)
        audio_path = tmp.name

    result = model.transcribe(audio_path)

    return result["text"].strip()

st.set_page_config(
    page_title="Voice AI SQL Assistant",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Voice & Text AI SQL Assistant")

st.markdown(
    """
Ask questions about your database using:

- 🎤 Voice
- ⌨️ Text

The application converts natural language into SQL,
executes it, and returns the result.
"""
)

audio = mic_recorder(
    start_prompt="🎙️ Start Recording",
    stop_prompt="⏹️ Stop Recording",
    key="mic"
)

transcribed_text = ""

if audio is not None:

    try:
        transcribed_text = speech_to_text(audio)

        if transcribed_text:

            st.session_state.user_query = transcribed_text

            st.success("Voice recognized successfully")

            with st.spinner("Analyzing query..."):

                result = get_sql_query_from_user_input(
                    transcribed_text
                )
                answer = f"Here's the analysis for your query:\n\n**{result}**"

            st.success("Analysis completed")
            st.markdown(answer)

            
    except Exception as e:

        st.error(f"Error transcribing audio: {e}")

user_query = st.text_area(
    "Ask a question about your database",
    value=st.session_state.user_query,
    height=120,
    placeholder="Example: Show all employees with salary greater than 50000"
)

st.session_state.user_query = user_query

user_query = st.session_state.user_query

if st.button("Analyze"):
    if user_query.strip() == "":
        st.warning("Please enter a question to analyze.")
        st.stop()
    else:
        with st.spinner("Analyzing your query..."):
            
            answer = get_sql_query_from_user_input(user_query)
            #answer = r"Here's the analysis for your query:\n\n**{user_query}**\n\n"
        
        st.success("Analysis complete!")
        st.markdown(answer)


st.markdown("""
    <style>
            .stApp {
             background-color:black;
             color: white;
}

textarea {
    font-size: 16px;
    padding: 10px;
    background-color: white;
    color: white;
}
    </style>
            
""", unsafe_allow_html=True)

#ui

import streamlit as st
from main import get_sql_query_from_user_input
from streamlit_mic_recorder import mic_recorder
import whisper
import tempfile
import os


# -----------------------------
# Load Whisper Model
# -----------------------------
@st.cache_res
def load_whisper():
    return whisper.load_model("base")


model = load_whisper()


# -----------------------------
# Session State
# -----------------------------
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

if "result" not in st.session_state:
    st.session_state.result = ""


# -----------------------------
# Speech To Text
# -----------------------------
def speech_to_text(audio):

    audio_bytes = audio.get("bytes")

    if not audio_bytes:
        return ""

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    ) as tmp:

        tmp.write(audio_bytes)
        audio_path = tmp.name

    result = model.transcribe(audio_path)

    return result["text"].strip()

st.set_page_config(
    page_title="Voice AI SQL Assistant",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Voice & Text AI SQL Assistant")

st.markdown(
    """
Ask questions about your database using:

- 🎤 Voice
- ⌨️ Text

The application converts natural language into SQL,
executes it, and returns the result.
"""
)

audio = mic_recorder(
    start_prompt="🎙️ Start Recording",
    stop_prompt="⏹️ Stop Recording",
    key="mic"
)

transcribed_text = ""

if audio is not None:

    try:
        transcribed_text = speech_to_text(audio)

        if transcribed_text:

            st.session_state.user_query = transcribed_text

            st.success("Voice recognized successfully")

            with st.spinner("Analyzing query..."):

                result = get_sql_query_from_user_input(
                    transcribed_text
                )
                answer = f"Here's the analysis for your query:\n\n**{result}**"

            st.success("Analysis completed")
            st.markdown(answer)

            
    except Exception as e:

        st.error(f"Error transcribing audio: {e}")

user_query = st.text_area(
    "Ask a question about your database",
    value=st.session_state.user_query,
    height=120,
    placeholder="Example: Show all employees with salary greater than 50000"
)

st.session_state.user_query = user_query

user_query = st.session_state.user_query

if st.button("Analyze"):
    if user_query.strip() == "":
        st.warning("Please enter a question to analyze.")
        st.stop()
    else:
        with st.spinner("Analyzing your query..."):
            
            answer = get_sql_query_from_user_input(user_query)
            #answer = r"Here's the analysis for your query:\n\n**{user_query}**\n\n"
        
        st.success("Analysis complete!")
        st.markdown(answer)


st.markdown("""
    <style>
            .stApp {
             background-color:black;
             color: white;
}

textarea {
    font-size: 16px;
    padding: 10px;
    background-color: white;
    color: white;
}
    </style>
            
""", unsafe_allow_html=True)"# AI-SQL-ASSISTANT" 
