import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found in .env file")

API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


# 🔹 Human signal check
def basic_human_check(text):
    if len(text.split()) < 15:
        return "⚠️ Very short text — result may be unreliable"

    if any(word in text.lower() for word in ["i ", "my ", "we ", "our "]):
        return "🧠 Human-like personal tone detected"

    return None


# 🔹 AI pattern check (IMPORTANT UPGRADE)
def ai_pattern_check(text):
    indicators = [
        "artificial intelligence (ai) is",
        "is a rapidly evolving field",
        "widely used in various domains",
        "plays an important role",
        "in conclusion",
        "machine learning is a subset",
        "has gained significant attention"
    ]

    score = sum(1 for phrase in indicators if phrase in text.lower())

    if score >= 2:
        return "🤖 Contains generic AI-style phrasing (textbook pattern detected)"

    return None


def analyze_text(text):
    prompt = f"""
You are an AI content analysis assistant.

IMPORTANT:
- High-quality writing does NOT mean human
- AI-generated text is often clear and well-structured
- Do NOT assume human just because grammar is good

Classify text into ONE of:
- Likely Human-written
- Likely AI-generated
- Uncertain

Focus on:
- Generic phrasing
- Textbook-style explanation
- Lack of personal experience
- Repetitive structure

Return format:

Classification:
Probability:
Reason:
Feedback:

Text:
{text}
"""

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        result = response.json()

        print("\n--- Raw API Response ---")
        print(result)

        if "choices" not in result:
            return f"❌ API Error: {result}"

        ai_output = result["choices"][0]["message"]["content"]

        # 🔥 Combine signals
        human_hint = basic_human_check(text)
        ai_hint = ai_pattern_check(text)

        final_output = "\n=== AI Analysis ===\n"
        final_output += ai_output

        if human_hint:
            final_output += f"\n\n🔍 Human Signal: {human_hint}"

        if ai_hint:
            final_output += f"\n🔍 AI Signal: {ai_hint}"

        final_output += "\n\n⚠️ Note: AI detection is probabilistic and may not be fully accurate."

        return final_output

    except Exception as e:
        return f"❌ Request failed: {str(e)}"


# 🚀 Main Program
if __name__ == "__main__":
    print("=== AI Academic Integrity Checker ===\n")

    user_text = input("Enter student text:\n")

    result = analyze_text(user_text)

    print("\n=== FINAL RESULT ===\n")
    print(result)
    print("\n✔ Analysis complete")