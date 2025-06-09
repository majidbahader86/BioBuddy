import streamlit as st
import requests
import os

# Backend API URL
API_URL = "http://127.0.0.1:8000"

# App Title
st.set_page_config(page_title="BioBuddy - Lab Assistant", page_icon="🧬")
st.title("🧬 BioBuddy Lab Assistant")

# --- Section 1: Ask a Lab-Related Question ---
st.header("🔬 Ask a Lab Question")

question = st.text_input("Enter your question here:")

if st.button("Get Answer"):
    if question.strip() == "":
        st.error("❌ Please enter a question.")
    else:
        with st.spinner("🤖 Getting answer from BioBuddy..."):
            try:
                response = requests.post(f"{API_URL}/ask/", params={"question": question})
                if response.status_code == 200:
                    answer = response.json().get("answer", "Sorry, no answer returned.")
                    st.success("💡 Answer:")
                    st.markdown(f"> {answer}")
                else:
                    st.error(f"⚠️ API Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Failed to connect to API: {e}")

st.markdown("---")

# --- Section 2: Upload Image for Disease Detection ---
st.header("🖼️ Upload Image for Prediction")

uploaded_file = st.file_uploader("Choose an image (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="🧾 Uploaded Image", use_container_width=True)

    if st.button("Predict Disease"):
        with st.spinner("🧠 Predicting disease from image..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                response = requests.post(f"{API_URL}/upload-image/", files=files)
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"🧬 Prediction: **{result['predicted_class']}**")
                    st.write(f"🔢 Confidence: **{result['confidence']}%**")
                else:
                    st.error(f"⚠️ API Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Failed to connect to API: {e}")
else:
    st.info("📎 Please upload an image to enable prediction.")

st.markdown("---")

# --- Section 3: View Prediction History ---
st.header("🗂️ Prediction History")

try:
    response = requests.get(f"{API_URL}/history/")
    if response.status_code == 200:
        history = response.json()
        if not history:
            st.info("📭 No prediction history found.")
        else:
            for record in reversed(history[-10:]):
                st.markdown(
                    f"📌 **{record['filename']}** → **{record['predicted_class']}** "
                    f"with **{record['confidence']}%** on `{record['timestamp']}`"
                )
    else:
        st.error("⚠️ Failed to fetch prediction history.")
except Exception as e:
    st.error(f"❌ Error connecting to API: {e}")
