# I am the central configuration file for my AI service.
# By keeping my settings here, I avoid hardcoding values across multiple files.

MODEL_NAME = "llama-3.3-70b-versatile"

# I'll add a default timeout for my Groq API calls to prevent hanging forever.
GROQ_TIMEOUT = 30.0
