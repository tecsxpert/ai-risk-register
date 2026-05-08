import os
import json
import logging
import time
from typing import Optional, Dict, Any
from groq import Groq
try:
    from groq.error import APIError, APIConnectionError, RateLimitError
except ImportError:
    # Fallback for different groq versions
    try:
        from groq._exceptions import APIError, APIConnectionError, RateLimitError
    except ImportError:
        # Generic exception fallback
        APIError = Exception
        APIConnectionError = Exception
        RateLimitError = Exception

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class GroqClient:
    """
    Enhanced Groq API client with retry logic, error handling, and JSON parsing.
    """
    
    def __init__(self, api_key: Optional[str] = None, max_retries: int = 3):
        """
        Initialize GroqClient.
        
        Args:
            api_key: Groq API key (defaults to GROQ_API_KEY env variable)
            max_retries: Maximum number of retry attempts (default: 3)
        """
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not provided in arguments or environment")
        
        self.client = Groq(api_key=self.api_key)
        self.max_retries = max_retries
        self.model = "llama3-8b-8192"
        logger.info("GroqClient initialized successfully")
    
    def _get_backoff_delay(self, attempt: int) -> float:
        """
        Calculate exponential backoff delay.
        
        Args:
            attempt: Current attempt number (0-indexed)
            
        Returns:
            Delay in seconds with exponential backoff
        """
        return min(2 ** attempt + (0.1 * attempt), 30)  # Max 30 seconds
    
    def get_ai_response(
        self,
        prompt: str,
        parse_json: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get AI response from Groq with retry logic and error handling.
        
        Args:
            prompt: The user prompt
            parse_json: Whether to parse response as JSON
            **kwargs: Additional parameters for chat completion
            
        Returns:
            Dict containing:
                - success: Boolean indicating if request succeeded
                - content: Response content
                - error: Error message if failed
                - retry_count: Number of retries attempted
        """
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Attempt {attempt + 1}/{self.max_retries}: Calling Groq API")
                
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model=self.model,
                    **kwargs
                )
                
                content = chat_completion.choices[0].message.content
                logger.info("API call successful")
                
                # Parse JSON if requested
                if parse_json:
                    try:
                        content = json.loads(content)
                        logger.info("JSON parsing successful")
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON parsing failed: {str(e)}", exc_info=True)
                        return {
                            "success": False,
                            "content": None,
                            "error": f"JSON parsing error: {str(e)}",
                            "retry_count": attempt
                        }
                
                return {
                    "success": True,
                    "content": content,
                    "error": None,
                    "retry_count": attempt
                }
                
            except RateLimitError as e:
                logger.warning(f"Rate limit error on attempt {attempt + 1}: {str(e)}")
                if attempt < self.max_retries - 1:
                    delay = self._get_backoff_delay(attempt)
                    logger.info(f"Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                else:
                    logger.error(f"Max retries ({self.max_retries}) exceeded due to rate limit")
                    return {
                        "success": False,
                        "content": None,
                        "error": f"Rate limit exceeded after {self.max_retries} retries",
                        "retry_count": attempt
                    }
                    
            except APIConnectionError as e:
                logger.warning(f"Connection error on attempt {attempt + 1}: {str(e)}")
                if attempt < self.max_retries - 1:
                    delay = self._get_backoff_delay(attempt)
                    logger.info(f"Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                else:
                    logger.error(f"Connection failed after {self.max_retries} retries")
                    return {
                        "success": False,
                        "content": None,
                        "error": f"API connection failed after {self.max_retries} retries: {str(e)}",
                        "retry_count": attempt
                    }
                    
            except APIError as e:
                logger.error(f"API error on attempt {attempt + 1}: {str(e)}", exc_info=True)
                if attempt < self.max_retries - 1:
                    delay = self._get_backoff_delay(attempt)
                    logger.info(f"Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                else:
                    logger.error(f"API error persisted after {self.max_retries} retries")
                    return {
                        "success": False,
                        "content": None,
                        "error": f"API error after {self.max_retries} retries: {str(e)}",
                        "retry_count": attempt
                    }
                    
            except Exception as e:
                logger.error(f"Unexpected error on attempt {attempt + 1}: {str(e)}", exc_info=True)
                return {
                    "success": False,
                    "content": None,
                    "error": f"Unexpected error: {str(e)}",
                    "retry_count": attempt
                }
        
        # This should not be reached but added for safety
        return {
            "success": False,
            "content": None,
            "error": "Max retries exceeded",
            "retry_count": self.max_retries - 1
        }


# Singleton instance for backward compatibility
_client_instance: Optional[GroqClient] = None

def get_client() -> GroqClient:
    """Get or create the singleton GroqClient instance."""
    global _client_instance
    if _client_instance is None:
        _client_instance = GroqClient()
    return _client_instance

def get_ai_response(prompt: str, parse_json: bool = False, **kwargs) -> Dict[str, Any]:
    """
    Convenience function for getting AI response using singleton client.
    
    Args:
        prompt: The user prompt
        parse_json: Whether to parse response as JSON
        **kwargs: Additional parameters for chat completion
        
    Returns:
        Dict with response data (see GroqClient.get_ai_response)
    """
    client = get_client()
    return client.get_ai_response(prompt, parse_json=parse_json, **kwargs)
