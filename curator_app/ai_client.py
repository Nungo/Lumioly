import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
load_dotenv()

# Configure the Gemini API client using the key from our .env file
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def get_explanation(query: str, model_name: str = "gemini-2.5-flash-preview-05-20"):
    """
    Query the Google Gemini API for an explanation.
    """
    if not GEMINI_API_KEY:
        return "Error: Google AI API key is not configured. Please check your .env file."

    try:
        # Initialize the generative model with the chosen model name
        model = genai.GenerativeModel(model_name)

        # Generate the content based on the user's query
        response = model.generate_content(query)

        return response.text

    except Exception as e:
        # Catch exceptions from the API call
        print(f"An error occurred during the Google Gemini API call: {e}")

        # Return a user-friendly error message to be displayed on the page
        return f"Error: The AI explanation could not be generated at this time. Details: {e}"
    
if __name__ == '__main__':
    if not GEMINI_API_KEY:
        print("API Key not found. Please set GOOGLE_API_KEY in your .env file.")
    else:
        print("Successfully configured Google AI. Testing with a sample query...")
        test_query = "Explain what a 'transformer architecture' is in the context of AI, in three sentences."
        print(f"\nSending query: '{test_query}'")

        explanation = get_explanation(test_query)

        print("\n--- Gemini's Explanation ---")
        print(explanation)
        print("--------------------------")