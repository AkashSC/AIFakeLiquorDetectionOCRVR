import streamlit as st
import requests
from PIL import Image
import io

# -----------------------------
# Voice Libraries
# -----------------------------
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode

# -----------------------------
# Load dataset
# -----------------------------
with open("sample_data/dataset.txt", "r") as f:
    dataset = [line.strip() for line in f.readlines()]

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="🍺 OCR + Voice Verifier", page_icon="🍺")
st.title("🍺 OCR + Voice Product Verifier")
st.write("Upload a product image or speak the product name to verify against dataset.")

# -----------------------------
# Image Upload & OCR
# -----------------------------
uploaded_file = st.file_uploader("Upload Image", type=["jpg","jpeg","png"])
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("Verify Product Image"):
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
                    st.success(f"Extracted Text: {parsed_text}")

                    matches = [p for p in dataset if parsed_text.lower() in p.lower()]
                    if matches:
                        st.success(f"✅ Product matches dataset: {matches}")
                    else:
                        st.warning("❌ No match found in dataset.")
                else:
                    st.error("OCR failed: No text detected.")
            else:
                error_message = result.get("ErrorMessage", "Unknown OCR API error")
                st.error(f"OCR failed: {error_message}")

        except Exception as e:
            st.error(f"OCR request failed: {str(e)}")

# -----------------------------
# Voice Verification
# -----------------------------
st.subheader("🎤 Voice Verification")

if st.button("Start Voice Verification"):
    st.info("Listening... Please speak the product name.")
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
        voice_text = recognizer.recognize_google(audio)
        st.success(f"You said: {voice_text}")

        matches = [p for p in dataset if voice_text.lower() in p.lower()]
        if matches:
            st.success(f"✅ Voice matches dataset: {matches}")
        else:
            st.warning("❌ No match found in dataset.")
    except sr.WaitTimeoutError:
        st.error("Listening timed out, please try again.")
    except Exception as e:
        st.error(f"Voice verification failed: {str(e)}")
