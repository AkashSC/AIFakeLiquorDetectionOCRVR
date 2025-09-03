import streamlit as st
from streamlit_javascript import st_javascript

st.title("🎤 Live Voice Transcription (Web Speech API)")

# Run JS in browser
text = st_javascript("""
() => {
  return new Promise((resolve, reject) => {
    try {
      var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        resolve("SpeechRecognition not supported in this browser.");
        return;
      }

      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = "en-US";

      let finalTranscript = "";

      recognition.onresult = (event) => {
        let interimTranscript = "";
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
          } else {
            interimTranscript += event.results[i][0].transcript;
          }
        }
        document.getElementById("transcript").innerText = finalTranscript + " " + interimTranscript;
      };

      recognition.onerror = (event) => {
        resolve("Error: " + event.error);
      };

      recognition.onend = () => {
        resolve(document.getElementById("transcript").innerText);
      };

      if (!document.getElementById("transcript")) {
        const div = document.createElement("div");
        div.id = "transcript";
        div.style = "margin-top:20px; font-size:16px; color:green;";
        document.body.appendChild(div);
      }

      recognition.start();
    } catch (err) {
      resolve("Exception: " + err.message);
    }
  });
}
""")

st.subheader("📝 Transcript")
st.write(text)
