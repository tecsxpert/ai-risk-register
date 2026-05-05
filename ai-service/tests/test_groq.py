# I am confirming the Groq API key is valid and the model responds correctly.
import os
import sys
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env at ai-service root
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
# I'm adding the ai-service root to the path so I can run this script directly.
sys.path.insert(0, BASE_DIR)
load_dotenv(os.path.join(BASE_DIR, '.env'))

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print(f"ERROR: GROQ_API_KEY is not set in {os.path.join(BASE_DIR, '.env')}")
    sys.exit(1)

client = Groq(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": "Say hello and state the model name you are running on."}
        ],
        temperature=0.3,
        max_tokens=100
    )
    content = response.choices[0].message.content
    print("SUCCESS: Groq API is working.")
    print(f"Response: {content}")
except Exception as e:
    print(f"ERROR: Groq API call failed: {e}")
    sys.exit(1)
