# I am testing the describe prompt against 5 realistic risk inputs to verify output quality.
import sys
import os
from dotenv import load_dotenv

# Add parent dir to path for imports
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, BASE_DIR)

from services.groq_client import call_groq

# Load environment variables from .env at ai-service root
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Load the prompt template
with open(os.path.join(BASE_DIR, 'prompts', 'describe_prompt.txt'), 'r') as f:
    template = f.read()

test_inputs = [
    "Unauthorised access to customer financial data via SQL injection in the login form",
    "Third-party cloud provider outage causing 4-hour downtime for all production systems",
    "Employee accidental deletion of critical database records without backup recovery plan",
    "Ransomware attack encrypting all HR files and demanding payment for decryption key",
    "Non-compliance with GDPR data retention policy due to legacy system limitations"
]

print("=== Describe Prompt Quality Test ===\n")
all_pass = True
for i, inp in enumerate(test_inputs, 1):
    # Note: Using 'describe' key as per existing groq_client implementation
    result = call_groq('describe', inp, temperature=0.3)
    if result is None:
        print(f"[FAIL] Test {i}: Groq returned None")
        all_pass = False
    else:
        # Check if result has description (existing implementation returns a dict)
        description = result.get('description', '')
        sentences = [s.strip() for s in description.split('.') if s.strip()]
        score = "PASS" if 2 <= len(sentences) <= 4 else "WARN"
        print(f"[{score}] Test {i}:\nInput: {inp[:60]}...\nOutput: {description}\n")

print("All tests passed." if all_pass else "Some tests failed — review and refine the prompt.")
