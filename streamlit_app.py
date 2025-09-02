import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, RTCConfiguration, WebRtcMode
import speech_recognition as sr
import av
import numpy as np

st.title("🎤 Live Voice Verification (Earphone/Mic Supported)")

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.buffer = bytes()
        self.sample_rate = 16000  # standard for Google Speech
        self.chunk_seconds = 2  # recognize every 2 seconds

    def recv_audio(self, frame: av.AudioFrame):
        # Convert audio frame → mono int16
        audio = frame.to_ndarray()
        if audio.ndim > 1:
            audio = np.mean(audio, axis=1).astype(np.int16)
        else:
            audio = audio.astype(np.int16)

        self.buffer += audio.tobytes()

        # Process when buffer >= chunk_seconds
        if len(self.buffer) > self.sample_rate * 2 * self.chunk_seconds:
            audio_data = sr.AudioData(self.buffer, self.sample_rate, 2)
            try:
                text = self.recognizer.recognize_google(audio_data)
                if "voice_text" not in st.session_state:
                    st.session_state["voice_text"] = []
                st.session_state["voice_text"].append(text)
            except sr.UnknownValueError:
                st.session_state["voice_text"].append("❌ Could not understand speech")
            except sr.RequestError:
                st.session_state["voice_text"].append("⚠️ Google API unavailable")
            self.buffer = bytes()  # reset after processing

        return frame

webrtc_streamer(
    key="speech",
    mode=WebRtcMode.SENDONLY,
    rtc_configuration=RTC_CONFIGURATION,
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
)

st.subheader("📝 Live Transcription:")
if "voice_text" in st.session_state:
    for line in st.session_state["voice_text"]:
        st.write(f"👉 {line}")
