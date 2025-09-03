import streamlit as st

st.set_page_config(page_title="🎤 Live Voice Verification")

st.title("🎤 Live Voice Verification")

st.markdown("Click **Start Listening** and allow microphone access when prompted.")

# Transcript placeholder
st.markdown("""
<div id="transcript-box" style="border:1px solid #ccc; padding:10px; margin-top:20px; min-height:50px;">
🎙 Speak something and your transcript will appear here...
</div>
""", unsafe_allow_html=True)

# Inject Web Speech API JS
st.markdown("""
<script>
let recognition;
let isListening = false;

function startListening() {
    if (!('webkitSpeechRecognition' in window)) {
        alert("Your browser does not support Web Speech API. Please use Chrome or Edge.");
        return;
    }

    recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    recognition.onresult = function(event) {
        let transcript = "";
        for (let i = event.resultIndex; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
        }
        const box = document.getElementById("transcript-box");
        if (box) {
            box.innerText = transcript;
        }
    };

    recognition.onerror = function(event) {
        console.error("Speech recognition error", event.error);
    };

    recognition.start();
    isListening = true;
}

function stopListening() {
    if (recognition && isListening) {
        recognition.stop();
        isListening = false;
        console.log("🎤 Voice recognition stopped");
    }
}

// Expose functions so Streamlit can call them
window.startListening = startListening;
window.stopListening = stopListening;
</script>
""", unsafe_allow_html=True)

# Use Streamlit buttons (they call JS via eval)
if st.button("▶️ Start Listening"):
    st.markdown("<script>startListening()</script>", unsafe_allow_html=True)

if st.button("⏹ Stop Listening"):
    st.markdown("<script>stopListening()</script>", unsafe_allow_html=True)
