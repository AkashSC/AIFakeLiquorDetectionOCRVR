import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, RTCConfiguration, WebRtcMode
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
        self.sample_rate = 16000  # standard speech recognition sample rate

    def recv_audio(self, frame: av.AudioFrame):
        # Convert audio frame to numpy int16
        audio = frame.to_ndarray().astype(np.int16).tobytes()
        self.buffer += audio

        # Process every ~3 seconds
        if len(self.buffer) > self.sample_rate * 2 * 3:  # 3 seconds of audio
            audio_data = sr.AudioData(self.buffer, self.sample_rate, 2)
            try:
                text = self.recognizer.recognize_google(audio_data)
                st.session_state["voice_text"] = text
            except sr.UnknownValueError:
                st.session_state["voice_text"] = "❌ Could not understand speech"
            except sr.RequestError:
                st.session_state["voice_text"] = "⚠️ Google API unavailable"
            self.buffer = bytes()  # reset buffer

        return frame

webrtc_streamer(
    key="speech",
    mode=WebRtcMode.SENDONLY,  # ✅ FIXED: use enum, not string
    rtc_configuration=RTC_CONFIGURATION,
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
)

if "voice_text" in st.session_state:
    st.success(f"✅ Recognized Speech: {st.session_state['voice_text']}")
