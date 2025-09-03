import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Live Voice Transcription", layout="centered")
st.title("🎤 Live Voice Transcription")

st.markdown("""
Press **Start Listening** below and speak.  
Your speech will be transcribed live in the text box.
""")

# JS to start/stop recognition
start_js = """
if (!window.recognition) {
    if (!('webkitSpeechRecognition' in window)) {
        alert('Your browser does not support Speech Recognition.');
    } else {
        window.recognition = new webkitSpeechRecognition();
        window.recognition.continuous = true;
        window.recognition.interimResults = true;
        window.recognition.lang = 'en-US';
        window.transcript = "";

        window.recognition.onresult = (event) => {
            let finalTranscript = '';
            let interimTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }
            window.transcript = finalTranscript + interimTranscript;
        };
    }
}
window.recognition.start();
'Listening started...';
"""

stop_js = """
if (window.recognition) {
    window.recognition.stop();
    'Listening stopped.';
} else {
    'Not running.';
}
"""

# Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start Listening"):
        streamlit_js_eval(js_code=start_js, key="start_js")
        st.info("Listening started...")

with col2:
    if st.button("⏹ Stop Listening"):
        streamlit_js_eval(js_code=stop_js, key="stop_js")
        st.warning("Listening stopped.")

# Display transcript
st.markdown("### 📝 Transcription")
transcript_text = streamlit_js_eval(js_code="window.transcript || ''", key="live_transcript")
st.text_area("Live Transcript", value=transcript_text or "", height=200)
