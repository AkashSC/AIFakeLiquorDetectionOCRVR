import streamlit as st
from streamlit_javascript import st_javascript

st.title("🎤 Live Voice Transcription")

# UI Buttons
start = st.button("▶️ Start Listening")
stop = st.button("⏹️ Stop Listening")

if start:
    text = st_javascript("""
    () => {
      return new Promise((resolve, reject) => {
        try {
          var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
          if (!SpeechRecognition) {
            resolve("SpeechRecognition not supported in this browser.");
            return;
          }

          if (!window.recognition) {
            window.recognition = new SpeechRecognition();
            window.recognition.continuous = true;
            window.recognition.interimResults = true;
            window.recognition.lang = "en-US";

            window.finalTranscript = "";

            window.recognition.onresult = (event) => {
              let interimTranscript = "";
              for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                  window.finalTranscript += event.results[i][0].transcript;
                } else {
                  interimTranscript += event.results[i][0].transcript;
                }
              }
              document.getElementById("transcript").innerText = window.finalTranscript + " " + interimTranscript;
            };
          }

          if (!document.getElementById("transcript")) {
            const div = document.createElement("div");
            div.id = "transcript";
            div.style = "margin-top:20px; font-size:16px; color:green;";
            document.body.appendChild(div);
          }

          window.recognition.start();
          resolve("Listening...");
        } catch (err) {
          resolve("Exception: " + err.message);
        }
      });
    }
    """)
    st.write(text)

if stop:
    text = st_javascript("""
    () => {
      return new Promise((resolve, reject) => {
        if (window.recognition) {
          window.recognition.stop();
          resolve(document.getElementById("transcript")?.innerText || "No transcript captured.");
        } else {
          resolve("Not started.");
        }
      });
    }
    """)
    st.subheader("📝 Transcript")
    st.write(text)
