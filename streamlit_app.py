import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import numpy as np
import whisper

st.set_page_config(page_title="🎤 Whisper Live Transcription")

st.title("🎤 Whisper Live Transcription")
model = whisper.load_model("base")  # can use "tiny", "small", etc.

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.buffer = []

    def recv_audio(self, frames, **kwargs):
        audio = np.frombuffer(frames.to_ndarray().tobytes(), np.int16).astype(np.float32) / 32768.0
        self.buffer.extend(audio.tolist())
        if len(self.buffer) > 16000 * 5:  # every 5s
            result = model.transcribe(np.array(self.buffer))
            st.session_state.transcript = result["text"]
            self.buffer = []
        return frames

webrtc_streamer(
    key="speech",
    mode="sendonly",
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
)

st.markdown("### Transcript")
st.write(st.session_state.get("transcript", "🎙 Waiting..."))
