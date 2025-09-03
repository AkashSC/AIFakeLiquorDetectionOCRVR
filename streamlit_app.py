import streamlit as st

st.set_page_config(page_title="🎤 Live Voice Verification")

st.title("🎤 Live Voice Verification")

st.markdown("""
Click **Start Listening** and allow microphone access when prompted.
""")

# Add a placeholder for transcript
transcript_box = st.empty()

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

    recognition.onstart = function() {
        console.log("🎤 Voice recognition started");
    };

    recognition.onresult = function(event) {
        let transcript = "";
        for (let i = event.resultIndex; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
        }
        const streamlitDoc = window.parent.document;
        let box = streamlitDoc.querySelector("#transcript-box");
        if (box) {
            box.innerText = transcript;
        }
    };

    recognition.onerror = function(event) {
        console.error("Speech recognition error", event.error);
    };

    recognition.onend = function() {
        console.log("Voice recognition ended");
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
</script>
""", unsafe_allow_html=True)

# Buttons
st.markdown("""
<div style="margin-top:20px;">
    <button onclick="startListening()">▶️ Start Listening</button>
    <button onclick="stopListening()">⏹ Stop Listening</button>
</div>
""", unsafe_allow_html=True)

# Transcript box
st.markdown("""
<div id="transcript-box" style="border:1px solid #ccc; padding:10px; margin-top:20px; min-height:50px;">
🎙 Speak something and your transcript will appear here...
</div>
""", unsafe_allow_html=True)
