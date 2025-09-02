import streamlit as st

st.set_page_config(page_title="Live Voice Verification", layout="centered")
st.title("🎤 Live Voice Verification (Browser-based)")

st.markdown("""
Click **Start Listening** and speak into your mic (earphones also work).  
Your speech will be transcribed live below 👇.
""")

# A placeholder for transcription
transcribed_text = st.empty()

# Inject JavaScript for browser speech recognition
st.markdown(
    """
    <script>
    var recognizing = false;
    var recognition = null;

    function startRecognition() {
        if (!('webkitSpeechRecognition' in window)) {
            alert("Your browser does not support live speech recognition.");
            return;
        }

        if (recognizing) {
            recognition.stop();
            recognizing = false;
            document.getElementById("stt_button").innerText = "Start Listening";
        } else {
            recognition = new webkitSpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = "en-US";

            recognition.onresult = function(event) {
                var transcript = "";
                for (var i = event.resultIndex; i < event.results.length; ++i) {
                    transcript += event.results[i][0].transcript;
                }
                // Send transcript back to Streamlit
                var streamlitDoc = window.parent.document;
                var textarea = streamlitDoc.querySelector('textarea[data-testid="stTextArea-input"]');
                textarea.value = transcript;
                textarea.dispatchEvent(new Event("input", { bubbles: true }));
            };

            recognition.start();
            recognizing = true;
            document.getElementById("stt_button").innerText = "Stop Listening";
        }
    }
    </script>
    """,
    unsafe_allow_html=True,
)

# Hidden text area to capture JS output
spoken_text = st.text_area("Live Transcription:", "", key="speech_text")

# Button to trigger JS
st.markdown(
    """
    <button id="stt_button" onclick="startRecognition()" style="padding:10px 20px; font-size:16px;">
        Start Listening
    </button>
    """,
    unsafe_allow_html=True,
)

# Show live result
if spoken_text:
    transcribed_text.success(f"🗣️ You said: {spoken_text}")
