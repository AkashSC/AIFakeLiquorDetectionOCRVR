import streamlit as st

st.set_page_config(page_title="🎤 Live Voice Verification")

st.title("🎤 Live Voice Verification")
st.markdown("Speak into your microphone. Your words will appear below:")

# Transcript placeholder
st.markdown("""
<div id="transcript-box" style="
    border:1px solid #ccc;
    padding:10px;
    margin-top:20px;
    min-height:80px;
    font-size:18px;
    background:#f9f9f9;
    white-space: pre-wrap;
">
🎙 Waiting for your voice...
</div>
""", unsafe_allow_html=True)

# Inject Web Speech API JS with permission handling
st.markdown("""
<script>
function startRecognition() {
    if (!('webkitSpeechRecognition' in window)) {
        document.getElementById("transcript-box").innerText =
            "❌ Web Speech API not supported. Use Chrome or Edge.";
        return;
    }

    try {
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "en-US";

        recognition.onresult = function(event) {
            let transcript = "";
            for (let i = 0; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript + " ";
            }
            const box = document.getElementById("transcript-box");
            if (box) {
                box.innerText = transcript.trim();
            }
        };

        recognition.onerror = function(event) {
            const box = document.getElementById("transcript-box");
            if (box) {
                box.innerText = "⚠️ Speech error: " + event.error;
            }
        };

        recognition.onend = function() {
            recognition.start(); // Auto restart
        };

        recognition.start();
        console.log("🎤 Speech recognition started");
    } catch (err) {
        document.getElementById("transcript-box").innerText =
            "⚠️ Could not start speech recognition: " + err;
    }
}

// Ensure it only runs once
if (!window.recognitionStarted) {
    window.recognitionStarted = true;
    startRecognition();
}
</script>
""", unsafe_allow_html=True)
