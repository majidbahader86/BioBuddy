import streamlit as st
import requests
from html import unescape
from PIL import Image
import os

# --- Set page config first ---
st.set_page_config(page_title="BioBuddy - Lab Assistant", page_icon="🧬", layout="centered")

API_URL = "http://127.0.0.1:8000"

# --- Image Upload Info ---
st.markdown("""
    <div style='background-color:#FFF3E0;padding:15px;border-radius:10px;border:1px solid #FFCC80;margin-bottom:10px'>
        <h4>🖼️ Image Classification (Experimental)</h4>
        <p>
            Upload a lab-related image (e.g., lab equipment, biological samples, or scientific illustrations).
            This is an experimental feature powered by <b>ResNet50</b> and may help identify common lab visuals.
        </p>
        <ul>
            <li>Accepted formats: <b>JPG, JPEG, PNG</b></li>
            <li>Max file size: <b>200MB</b></li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Add a disclaimer
st.markdown(
    "<p style='font-size: 12px; color: #888;'>Note: This is a general-purpose AI model not trained specifically on lab images. Results may vary.</p>",
    unsafe_allow_html=True
)

# Load logo 
logo_path = "static/logo.png"  # Place your logo in static/logo.png
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.image(logo, width=100)

st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>🧬 BioBuddy: Lab & AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Your smart companion for navigating wet lab protocols and science questions.</p>", unsafe_allow_html=True)

# Store chat history in session
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []

# --- Input Section ---
st.subheader("🔬 Ask a Question")
question = st.text_area("💬 Enter your lab question:", height=100)

if st.button("🚀 Submit"):
    if not question.strip():
        st.warning("⚠️ Please enter a question first.")
    else:
        with st.spinner("🤖 BioBuddy is thinking..."):
            try:
                response = requests.post(f"{API_URL}/ask/", json={"question": question})
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer returned.")
                    cleaned_answer = unescape(answer).replace("<br>", "\n")

                    # Show the answer in a styled blue box
                    st.markdown(
                        f"""
                        <div style='background-color:#e6f7ff; padding:15px; border-radius:10px; border:1px solid #bee3f8;'>
                            <b>💡 BioBuddy says:</b><br>{cleaned_answer}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Save to history
                    st.session_state.qa_history.append({"q": question, "a": cleaned_answer})
                else:
                    st.error(f"⚠️ API Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Failed to connect to API: {e}")

# --- Chat History Display ---
if st.session_state.qa_history:
    st.markdown("---")
    st.subheader("📂 Previous Questions & Answers")
    for record in reversed(st.session_state.qa_history[-5:]):
        st.markdown(f"""
        <div style='padding:10px;border:1px solid #ccc;border-radius:10px;margin-bottom:15px;background:#f9f9f9'>
            <b>❓ Q:</b> {record['q']}<br>
            <b>💡 A:</b><br><pre style='white-space: pre-wrap;'>{record['a']}</pre>
        </div>
        """, unsafe_allow_html=True)

# --- Image Upload Section ---
st.markdown("---")
st.subheader("🖼️ Image Classification (Experimental)")

st.markdown("""
Upload a lab-related image (e.g., samples, equipment, or scientific illustrations) and let BioBuddy try to identify it using ResNet50.
""")

uploaded_file = st.file_uploader("📎 Upload an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

if st.button("🧠 Analyze Image"):
    if uploaded_file is None:
        st.warning("⚠️ Please upload an image before submitting.")
    else:
        with st.spinner("🔍 Analyzing image..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                response = requests.post(f"{API_URL}/upload-image/", files=files)
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Image classified successfully!")
                    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

                    st.markdown(f"""
                        <div style='background-color:#f1f8e9;padding:15px;border-radius:10px;margin-top:15px;border:1px solid #c5e1a5;'>
                            <b>🔎 Prediction:</b> {result['predicted_class']}<br>
                            <b>📊 Confidence:</b> {result['confidence_percent']}%
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"❌ API Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Could not connect to API: {e}")

