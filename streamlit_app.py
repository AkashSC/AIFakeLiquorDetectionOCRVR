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
    min-height:50px;
    font-size:18px;
    background:#f9f9f9;
">
🎙 Waiting for your voice...
</div>
""", unsafe_allow_html=True)

# Inject Web Speech API JS
st.markdown("""
<script>
if (!('webkitSpeechRecognition' in window)) {
    document.getElementById("transcript-box").innerText =
        "❌ Your browser does not support Web Speech API. Use Chrome or Edge.";
} else {
    const recognition = new webkitSpeechRecognition();
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
        const box = document.getElementById("transcript-box");
        if (box) {
            box.innerText = "⚠️ Error: " + event.error;
        }
    };

    recognition.onend = function() {
        recognition.start(); // auto-restart
    };

    recognition.start();
}
</script>
""", unsafe_allow_html=True)
