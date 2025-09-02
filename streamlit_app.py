import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, RTCConfiguration
import speech_recognition as sr
import av
import numpy as np

st.title("🎤 Live Voice Verification")

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.buffer = bytes()
        self.sample_rate = 16000  # standard speech rate

    def recv_audio(self, frame: av.AudioFrame):
        # Convert audio frame to numpy int16
        audio = frame.to_ndarray().astype(np.int16).tobytes()
        self.buffer += audio

        # Process when enough audio collected
        if len(self.buffer) > self.sample_rate * 2 * 3:  # 3 seconds of audio
            audio_data = sr.AudioData(self.buffer, self.sample_rate, 2)
            try:
                text = self.recognizer.recognize_google(audio_data)
                st.session_state["voice_text"] = text
            except sr.UnknownValueError:
                st.session_state["voice_text"] = "Could not understand"
            except sr.RequestError:
                st.session_state["voice_text"] = "API unavailable"
            # reset buffer
            self.buffer = bytes()

        return frame

webrtc_streamer(
    key="speech",
    mode="sendonly",
    rtc_configuration=RTC_CONFIGURATION,
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
)

if "voice_text" in st.session_state:
    st.write("✅ Recognized:", st.session_state["voice_text"])
