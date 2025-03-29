import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

def generate_reply(user_message: str):
    response = model.generate_content(user_message)
    return response.text

if __name__ == "__main__":
    print("🔁 Testing response generation with Gemini...")
    prompt = "Hello! How are you doing?"
    result = generate_reply(prompt)
    print("Model response:\n", result)