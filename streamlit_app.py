import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, RTCConfiguration
import speech_recognition as sr
import av

st.title("🎤 Live Voice Verification")

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recv_audio(self, frame: av.AudioFrame):
        audio = frame.to_ndarray().flatten().astype("int16")
        # Convert raw audio to WAV for SpeechRecognition
        with sr.AudioData(audio.tobytes(), frame.sample_rate, 2) as source:
            try:
                text = self.recognizer.recognize_google(source)
                st.session_state["voice_text"] = text
            except sr.UnknownValueError:
                st.session_state["voice_text"] = "Could not understand"
        return frame

webrtc_streamer(
    key="speech",
    mode="sendonly",
    rtc_configuration=RTC_CONFIGURATION,
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
)

if "voice_text" in st.session_state:
    st.write("Recognized:", st.session_state["voice_text"])
