import os
import re
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


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
    Uses the new google.genai SDK.
    """

    if not GEMINI_API_KEY:
        return "API key not configured. Please add GEMINI_API_KEY to your .env file."

    prompted_query = f"""You are Glintly AI, a friendly assistant inside a clean chat interface.
Answer in 3-5 sentences max. Be conversational and direct.
Use plain text only — no bullet points, no bold, no markdown, no asterisks, no headings.
Just natural, clear sentences as if explaining to a smart friend.

Question: {query}"""

    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model=model_name,
            contents=prompted_query
        )

        # Safely extract text (new SDK can structure output)
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
        print("Testing Glintly AI...")
        result = get_explanation("What is Hugging Face Transformers?")
        print(result)
