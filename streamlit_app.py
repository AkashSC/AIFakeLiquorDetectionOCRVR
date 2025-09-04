import json
import requests
import streamlit as st
from PIL import Image
import streamlit.components.v1 as components

# -----------------------------
# Load dataset
# -----------------------------
with open("dataset.txt", "r") as f:
    DATASET = [line.strip() for line in f if line.strip()]

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="🍺 Product Verifier", page_icon="🍺")
st.title("🍺 Fake Liquor Detection")
st.write("Verify a product by **OCR (upload image)** or **Speech Recognition (talk)**.")

mode = st.radio("Choose Verification Mode:", ["OCR (Image Upload)", "Speech Recognition"])

# -----------------------------
# OCR Mode (uses your working code)
# -----------------------------
if mode == "OCR (Image Upload)":
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        if st.button("Verify Product"):
            st.info("Running OCR, please wait...")

            try:
                # Send the file with proper filename and content type
                files = {
                    "filename": (uploaded_file.name, uploaded_file, uploaded_file.type)
                }
                data = {"apikey": "helloworld", "language": "eng"}

                response = requests.post(
                    "https://api.ocr.space/parse/image",
                    files=files,
                    data=data,
                    timeout=60,
                )
                result = response.json()

                if "ParsedResults" in result and result["ParsedResults"]:
                    parsed_text = result["ParsedResults"][0].get("ParsedText", "").strip()

                    if parsed_text:
                        st.success(f"📄 Extracted Text: {parsed_text}")

                        # simple case-insensitive containment match
                        matches = [p for p in DATASET if parsed_text.lower() in p.lower() or p.lower() in parsed_text.lower()]
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
# Speech Recognition Mode (pure browser, runs inside a component iframe)
# -----------------------------
else:
    st.markdown("**Tip:** Use Chrome/Edge desktop or Android (Web Speech API).")

    dataset_js = json.dumps(DATASET)  # embed Python dataset into JS

    components.html(f"""
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <style>
      body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; }}
      .btn {{
        padding:10px 16px; margin:4px; border:none; border-radius:8px; cursor:pointer; font-size:14px;
      }}
      .start {{ background:#16a34a; color:white; }}
      .stop {{ background:#dc2626; color:white; }}
      .verify {{ background:#2563eb; color:white; }}
      #output {{
        border:1px solid #ddd; border-radius:8px; padding:10px; min-height:88px; font-size:16px; background:#fafafa;
        white-space:pre-wrap; margin-top:8px;
      }}
      #result {{
        margin-top:10px; font-weight:600;
      }}
    </style>
  </head>
  <body>
    <h3>🎤 Speak the Product Name</h3>
    <p>Click <b>Start</b>, say the product name, then click <b>Verify</b> to match against the dataset.</p>

    <div>
      <button class="btn start" id="btnStart">▶ Start Listening</button>
      <button class="btn stop" id="btnStop">⏹ Stop</button>
      <button class="btn verify" id="btnVerify">🔎 Verify</button>
    </div>

    <div id="output">🎙 Waiting...</div>
    <div id="result"></div>

    <script>
      // Embed dataset from Python
      const DATASET = {dataset_js}.map(s => s.toLowerCase());

      // Simple match function
      function matchTranscript(t) {{
        const text = (t || "").toLowerCase().trim();
        if (!text) return "Please speak first.";
        const matches = DATASET.filter(p => p.includes(text) || text.includes(p));
        return matches.length ? ("✅ Match found: " + matches.join(", ")) : "❌ No match found.";
      }}

      // Web Speech API
      let recognition = null;
      let lastTranscript = "";

      function supported() {{
        return ("webkitSpeechRecognition" in window);
      }}

      function startRecognition() {{
        if (!supported()) {{
          showOutput("❌ Web Speech API not supported. Use Chrome/Edge.");
          return;
        }}
        try {{
          recognition = new webkitSpeechRecognition();
          recognition.continuous = true;
          recognition.interimResults = true;
          recognition.lang = "en-US";

          recognition.onresult = (event) => {{
            let t = "";
            for (let i = 0; i < event.results.length; i++) {{
              t += event.results[i][0].transcript + " ";
            }}
            lastTranscript = t.trim();
            showOutput(lastTranscript || "🎙 Listening…");
          }};

          recognition.onerror = (e) => {{
            showOutput("⚠️ Speech error: " + e.error);
          }};

          recognition.onend = () => {{
            // keep it simple: don't auto-restart; user controls start/stop
          }};

          recognition.start();
          showOutput("🎙 Listening…");
        }} catch (err) {{
          showOutput("⚠️ Could not start recognition: " + err);
        }}
      }}

      function stopRecognition() {{
        if (recognition) {{
          recognition.stop();
          recognition = null;
          showOutput(lastTranscript || "⏹ Stopped.");
        }}
      }}

      function verifyNow() {{
        const res = matchTranscript(lastTranscript);
        document.getElementById("result").textContent = res;
      }}

      function showOutput(txt) {{
        const box = document.getElementById("output");
        if (box) box.textContent = txt;
      }}

      // Wire up buttons (works inside component iframe)
      document.getElementById("btnStart").addEventListener("click", startRecognition);
      document.getElementById("btnStop").addEventListener("click", stopRecognition);
      document.getElementById("btnVerify").addEventListener("click", verifyNow);

      // Initial support check
      if (!supported()) {{
        showOutput("❌ Web Speech API not supported. Please use Chrome/Edge.");
      }}
    </script>
  </body>
</html>
    """, height=380, scrolling=False)
