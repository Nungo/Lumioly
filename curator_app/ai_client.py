import os
import re
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

SYSTEM_PROMPT = """You are Lumioly AI, the intelligent assistant built into Lumioly — an AI news and tools intelligence platform.

Your role is strictly to help users understand:
- Artificial intelligence news, research, and developments
- AI tools, models, and platforms
- Machine learning and deep learning concepts
- Tech industry news related to AI
- How to use or evaluate specific AI products

If the user asks about anything outside these topics — food, sports, personal advice, entertainment, general knowledge, creative writing, or anything unrelated to AI and technology — respond with exactly this:
"I'm Lumioly AI, focused specifically on artificial intelligence news and tools. For that question you'd be better served by a general assistant. Try asking me about the latest AI developments, a specific tool, or how a machine learning concept works!"

Never break this rule regardless of how the question is phrased or what the user claims.
Answer in 3-5 sentences max. Be conversational and direct.
Use plain text only — no bullet points, no bold, no markdown, no asterisks, no headings.
Just natural, clear sentences as if explaining to a smart friend."""


def clean_markdown(text: str) -> str:
    """Strip markdown so responses render cleanly as plain text in HTML."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'^\s*\*\s+', '• ', text, flags=re.MULTILINE)
    text = re.sub(r'#{1,6}\s+', '', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    return text.strip()


def get_explanation(query: str, model_name: str = "gemini-2.5-flash-lite"):
    """
    Query Gemini for a short, conversational explanation.
    Restricted to AI and technology topics only.
    Uses the new google.genai SDK.
    """

    if not GEMINI_API_KEY:
        return "API key not configured. Please add GEMINI_API_KEY to your .env file."

    full_prompt = f"{SYSTEM_PROMPT}\n\nUser question: {query}"

    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model=model_name,
            contents=full_prompt
        )

        if hasattr(response, "text") and response.text:
            output_text = response.text
        elif hasattr(response, "candidates") and response.candidates:
            output_text = response.candidates[0].content.parts[0].text
        else:
            return "I couldn't generate a response right now."

        return clean_markdown(output_text)

    except Exception as e:
        error_str = str(e)
        print(f"Gemini API error: {e}")

        if "429" in error_str or "quota" in error_str.lower() or "exhausted" in error_str.lower():
            return "I've hit my request limit for now — try again in a few minutes."
        elif "403" in error_str or "api key" in error_str.lower():
            return "There's an issue with the API key. Please check your .env file."
        elif "404" in error_str or "not found" in error_str.lower():
            return "The AI model couldn't be reached. Please try again shortly."
        else:
            return "I couldn't generate a response right now. Please try again in a moment."


if __name__ == '__main__':
    if not GEMINI_API_KEY:
        print("API Key not found. Set GEMINI_API_KEY in your .env file.")
    else:
        print("Testing Lumioly AI topic restriction...")
        print("\n-- AI question --")
        print(get_explanation("What is Hugging Face Transformers?"))
        print("\n-- Off-topic question --")
        print(get_explanation("What is the best chicken recipe?"))