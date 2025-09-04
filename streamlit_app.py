import streamlit as st
import requests
from PIL import Image

# -----------------------------
# Load dataset
# -----------------------------
with open("dataset.txt", "r") as f:
    dataset = [line.strip() for line in f.readlines()]

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="🍺 Product Verifier", page_icon="🍺")

st.title("🍺 Fake Liquor Detection")
st.write("Verify product either by **OCR (upload image)** or **Speech Recognition (talk)**")

mode = st.radio("Choose Verification Mode:", ["OCR (Image Upload)", "Speech Recognition"])

# -----------------------------
# OCR Mode
# -----------------------------
if mode == "OCR (Image Upload)":
    uploaded_file = st.file_uploader("Upload Image", type=["jpg","jpeg","png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        if st.button("Verify Product"):
            st.info("Running OCR, please wait...")

            try:
                files = {
                    "filename": (uploaded_file.name, uploaded_file, uploaded_file.type)
                }
                data = {"apikey": "helloworld", "language": "eng"}

                response = requests.post(
                    "https://api.ocr.space/parse/image",
                    files=files,
                    data=data
                )

                result = response.json()

                if "ParsedResults" in result and result["ParsedResults"]:
                    parsed_text = result["ParsedResults"][0].get("ParsedText", "").strip()

                    if parsed_text:
                        st.success(f"📄 Extracted Text: {parsed_text}")

                        matches = [p for p in dataset if parsed_text.lower() in p.lower()]
                        if matches:
                            st.success(f"✅ Product matches dataset: {matches}")
                        else:
                            st.warning("❌ No match found in dataset.")
                    else:
                        st.error("OCR failed: No text detected in image.")
                else:
                    error_message = result.get("ErrorMessage", "Unknown error from OCR API")
                    st.error(f"OCR failed: {error_message}")

            except Exception as e:
                st.error(f"OCR request failed: {str(e)}")


# -----------------------------
# Speech Recognition Mode
# -----------------------------
elif mode == "Speech Recognition":
    st.markdown("""
    <h3>🎤 Speak the Product Name</h3>
    <p>Click <b>Start Listening</b> and say the product name clearly. The transcript will appear below.</p>
    
    <button onclick="startRecognition()" 
        style="padding:10px 20px;margin:5px;background:green;color:white;border:none;border-radius:5px;">
        ▶ Start Listening
    </button>
    <button onclick="stopRecognition()" 
        style="padding:10px 20px;margin:5px;background:red;color:white;border:none;border-radius:5px;">
        ⏹ Stop
    </button>

    <div id="output" style="border:1px solid #ccc;margin-top:20px;padding:10px;
        font-size:18px;min-height:80px;">🎙 Waiting...</div>

    <script>
      let recognition;
      function startRecognition() {
        if (!("webkitSpeechRecognition" in window)) {
          document.getElementById("output").innerText = 
            "❌ Web Speech API not supported. Use Chrome/Edge.";
          return;
        }
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "en-US";
        recognition.onresult = (event) => {
          let transcript = "";
          for (let i = 0; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript + " ";
          }
          transcript = transcript.trim();
          document.getElementById("output").innerText = transcript;

          // send transcript to Streamlit
          const streamlitInput = window.parent.document.querySelector('input[data-testid="stTextInput"]');
          if (streamlitInput) {
            streamlitInput.value = transcript;
            streamlitInput.dispatchEvent(new Event("input", { bubbles: true }));
          }
        };
        recognition.onerror = (event) => {
          document.getElementById("output").innerText = "⚠️ Error: " + event.error;
        };
        recognition.start();
      }
      function stopRecognition() {
        if (recognition) recognition.stop();
      }
    </script>
    """, unsafe_allow_html=True)

    transcript = st.text_input("Transcript (auto-filled when you speak)")

    if transcript:
        st.success(f"📄 You said: {transcript}")
        matches = [p for p in dataset if transcript.lower() in p.lower()]
        if matches:
            st.success(f"✅ Product matches dataset: {matches}")
        else:
            st.warning("❌ No match found in dataset.")
