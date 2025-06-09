import streamlit as st
import requests
from html import unescape

API_URL = "http://127.0.0.1:8000"

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
                response = requests.post(f"{API_URL}/ask/", json={"question": question})
                if response.status_code == 200:
                    data = response.json()
                    if "answer" in data:
                        st.success("💡 Answer:")
                        st.markdown(unescape(data["answer"]), unsafe_allow_html=True)
                    else:
                        st.warning("🤔 No answer returned.")
                else:
                    st.error(f"⚠️ API Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Failed to connect to API: {e}")

st.markdown("---")

# --- Section 2: Upload Image for Disease Detection ---
st.header("🖼️ Upload Lab Image for Analysis")

st.markdown(
    "Drag and drop or select an image file (JPG, JPEG, PNG) to classify lab images.\n\n"
    "Maximum file size: 200MB"
)

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="🧾 Uploaded Image Preview", use_container_width=True)

    if st.button("Classify Image"):
        with st.spinner("🧠 Classifying image..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                response = requests.post(f"{API_URL}/upload-image/", files=files)
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"🧬 Prediction: **{result.get('predicted_class', 'N/A')}**")
                    st.write(f"🔢 Confidence: **{result.get('confidence_percent', 'N/A')}%**")
                else:
                    st.error(f"⚠️ API Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Failed to connect to API: {e}")

    st.info(
        "Note: This is a demo model using general image classification (ResNet50). "
        "Future versions will support lab image analysis like gel bands and western blots."
    )
else:
    st.info("📎 Please upload an image to enable prediction.")

st.markdown("---")

# --- Section 3: Option to show Prediction History ---
if st.checkbox("Show Prediction History"):
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
                        f"📌 **{record.get('filename', 'Unknown')}** → **{record.get('predicted_class', 'N/A')}** "
                        f"with **{record.get('confidence_percent', 'N/A')}%** on `{record.get('timestamp', 'Unknown')}`"
                    )
        else:
            st.error("⚠️ Failed to fetch prediction history.")
    except Exception as e:
        st.error(f"❌ Error connecting to API: {e}")
