import os
import json
import time
import logging
from groq import Groq
from dotenv import load_dotenv

# Loading my environment variables first so I can safely read my API key
load_dotenv()

logger = logging.getLogger(__name__)

# Initializing the client carefully. Never put the API key string directly here!
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Pointing to my prompts folder which sits next to the services folder
PROMPT_DIR = os.path.join(os.path.dirname(__file__), '..', 'prompts')

def load_prompt(key: str) -> str:
    # Dynamically reading my prompt text files
    path = os.path.join(PROMPT_DIR, f'{key}_prompt.txt')
    with open(path) as f:
        return f.read()

def call_groq(prompt_key, user_input, temperature=0.3, max_retries=3) -> dict | None:
    # I'll load the prompt template and inject the user's input directly into it
    template = load_prompt(prompt_key)
    full_prompt = template.replace('{user_input}', user_input)
    
    # My 3-retry loop to handle the free tier API hiccups and rate limiting
    for attempt in range(max_retries):
        try:
            # I must use this exact model! Any typo will cause a silent error.
            resp = client.chat.completions.create(
                model='llama-3.3-70b-versatile',
                messages=[{'role': 'user', 'content': full_prompt}],
                temperature=temperature,
                max_tokens=1000
            )
            raw = resp.choices[0].message.content.strip()
            
            # The model sometimes throws in markdown code blocks, so I'll strip them out just to be safe
            if raw.startswith('```'):
                if '\n' in raw:
                    raw = raw.split('\n', 1)[1]
                if raw.endswith('```'):
                    if '\n' in raw:
                        raw = raw.rsplit('\n', 1)[0]
                    else:
                        raw = raw[:-3]
            
            # Remove 'json' if present
            if raw.strip().lower().startswith('json'):
                raw = raw.strip()[4:].strip()
                
            # Now I'll parse it into my requested JSON shape
            return json.loads(raw.strip())
            
        except json.JSONDecodeError as e:
            logger.error(f'JSON error attempt {attempt+1}: {e}')
            # If we've exhausted our retries, time to bail out
            if attempt == max_retries - 1:
                return None
        except Exception as e:
            logger.error(f'Groq error attempt {attempt+1}: {e}')
            # Giving the API some breathers with 1s, 2s, 4s backoff sleep
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                return None
    return None
