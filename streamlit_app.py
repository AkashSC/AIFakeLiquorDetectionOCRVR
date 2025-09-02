import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Live Voice Transcription", layout="centered")
st.title("🎤 Live Voice Transcription")

st.markdown("""
Press **Start Listening** below and speak.  
Your speech will be transcribed live in the text box.
""")

# JS code to capture live speech using browser Web Speech API
js_code = """
let recognition;
let isListening = false;

async function startListening() {
    if (!('webkitSpeechRecognition' in window)) {
        alert('Your browser does not support Speech Recognition.');
        return '';
    }
    recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    let finalTranscript = '';
    recognition.onresult = (event) => {
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

    recognition.start();
    isListening = true;
    return 'Listening started...';
}

async function stopListening() {
    if (recognition && isListening) {
        recognition.stop();
        isListening = false;
        return 'Listening stopped.';
    }
    return 'Was not listening.';
}

return {startListening: startListening, stopListening: stopListening};
"""

# Initialize JS functions
js_funcs = streamlit_js_eval(js_code=js_code, key="js_funcs", return_value=True)

# Buttons to start/stop
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start Listening"):
        msg = js_funcs["startListening"]()
        st.info(msg)

with col2:
    if st.button("⏹ Stop Listening"):
        msg = js_funcs["stopListening"]()
        st.warning(msg)

# Display live transcription
st.markdown("### 📝 Transcription")
transcript_text = streamlit_js_eval(js_code="window.transcript || ''", key="live_transcript")
st.text_area("Live Transcript", value=transcript_text, height=200)
