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
                    answer = data.get("answer", "No answer returned.")
                    st.success("💡 Answer:")
                    st.markdown(unescape(answer), unsafe_allow_html=True)
                else:
                    st.error(f"⚠️ API Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Failed to connect to API: {e}")

st.markdown("---")

# --- Optional: Show History ---
show_history = st.checkbox("Show Q&A History")

if show_history:
    st.header("🗂️ Q&A History")
    try:
        response = requests.get(f"{API_URL}/history/")
        if response.status_code == 200:
            history = response.json()
            if not history:
                st.info("📭 No history found.")
            else:
                for record in reversed(history[-10:]):
                    if record.get("type") == "question":
                        st.markdown(
                            f"❓ **Q:** {record['question']}\n\n"
                            f"💡 **A:** {record['answer']}\n\n"
                            f"_at {record['timestamp']}_"
                        )
        else:
            st.error("⚠️ Failed to fetch history.")
    except Exception as e:
        st.error(f"❌ Error connecting to API: {e}")
