import os
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

# Get the path to the .env file in the root directory
current_dir = Path(__file__).parent
dotenv_path = current_dir.parent / '.env'

print(f"Looking for .env at: {dotenv_path.absolute()}")

if not dotenv_path.exists():
    print(f"Error: .env file does not exist at {dotenv_path.absolute()}")
    exit(1)

load_dotenv(dotenv_path=dotenv_path)

api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    print("Error: GROQ_API_KEY not found in environment variables after loading .env")
    exit(1)

print(f"API Key found: {api_key[:10]}...")

client = Groq(api_key=api_key)

try:
    print("Sending request to Groq...")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Explain the importance of fast language models in 20 words.",
            }
        ],
        model="llama3-8b-8192",
    )
    print("API Call Successful!")
    print("Response:", chat_completion.choices[0].message.content)
except Exception as e:
    print("API Call Failed!")
    print("Error Type:", type(e).__name__)
    print("Error Message:", str(e))
