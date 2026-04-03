import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load env
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def basic_human_check(text):
    if len(text.split()) < 15:
        return "⚠️ Very short text — result may be unreliable"
    if any(word in text.lower() for word in ["i ", "my ", "we ", "our "]):
        return "🧠 Human-like personal tone detected"
    return None


def analyze_text(text):
    prompt = f"""
You are an AI detection assistant.

Classify text as:
- Human-written
- AI-generated
- Uncertain

Rules:
- Grammar mistakes ≠ AI
- Simple writing ≠ AI
- Only mark AI if highly structured or robotic

Return:
1. Classification
2. Probability (0-100%)
3. Reason
4. Feedback

Text:
{text}
"""

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=data)
    result = response.json()

    if "choices" not in result:
        return f"❌ API Error: {result}"

    output = result["choices"][0]["message"]["content"]

    hint = basic_human_check(text)

    if hint:
        output += f"\n\n🔍 Insight: {hint}"

    return output


# 🎨 UI
st.set_page_config(page_title="AI Integrity Checker", layout="centered")

st.title("🧠 AI Academic Integrity Checker")
st.markdown("Detect whether text is AI-generated or human-written")

text = st.text_area("✍️ Enter student text here:", height=200)

if st.button("🔍 Analyze"):
    if text.strip() == "":
        st.warning("Please enter some text")
    else:
        with st.spinner("Analyzing..."):
            result = analyze_text(text)

        st.success("Analysis Complete ✅")
        st.markdown("### 📊 Result:")
        st.write(result)