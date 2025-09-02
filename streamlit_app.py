import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Live Voice Verification", layout="centered")
st.title("🎤 Live Voice Verification (Browser-based)")

st.markdown("""
Click **Start Listening** and speak into your mic (earphones also work).  
Your speech will be transcribed live below 👇.
""")

# Run JavaScript in browser and get live transcript
js_code = """
async function listen() {
    return new Promise((resolve, reject) => {
        if (!('webkitSpeechRecognition' in window)) {
            alert("Your browser does not support live speech recognition.");
            reject("Not supported");
        }

        const recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "en-US";

        recognition.onresult = function(event) {
            let transcript = "";
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                transcript += event.results[i][0].transcript;
            }
            resolve(transcript);
        };

        recognition.onerror = function(event) {
            reject(event.error);
        };

        recognition.start();
    });
}

listen();
"""

# Button triggers JS evaluation
if st.button("Start Listening"):
    transcript = streamlit_js_eval(js_code=js_code)
    if transcript:
        st.success(f"🗣️ You said: {transcript}")
