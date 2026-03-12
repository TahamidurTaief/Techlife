import os
import logging
from groq import Groq

logger = logging.getLogger(__name__)


def _get_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment variables.")
    return Groq(api_key=api_key)


def check_adult_content(title: str, content: str) -> bool:
    """
    Returns True if adult/harmful content detected, False otherwise.
    Fail-safe: returns False on API error (don't block the user).
    """
    try:
        client = _get_client()
        prompt = f"""You are a strict content moderation system.
Analyze the following blog post and determine if it contains adult, sexual, violent, hateful, or harmful content.

Title: {title}
Content: {content[:3000]}

Reply with ONLY one word: YES or NO."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5,
            temperature=0,
        )
        answer = response.choices[0].message.content.strip().upper()
        return answer == "YES"

    except Exception as e:
        logger.error(f"[Groq] Adult content check failed: {e}")
        return False


def check_copyright(title: str, content: str) -> bool:
    """
    Returns True if content appears copied/plagiarized, False otherwise.
    Fail-safe: returns False on API error.
    """
    try:
        client = _get_client()
        prompt = f"""You are a plagiarism detection expert.
Analyze the following blog post. Does this content appear to be copied, plagiarized, or directly taken from another well-known source without original contribution?

Title: {title}
Content: {content[:3000]}

Consider: generic filler text, obvious copy-paste patterns, well-known copyrighted passages.
Reply with ONLY one word: YES or NO."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5,
            temperature=0,
        )
        answer = response.choices[0].message.content.strip().upper()
        return answer == "YES"

    except Exception as e:
        logger.error(f"[Groq] Copyright check failed: {e}")
        return False


def get_quality_score(title: str, content: str) -> int:
    """
    Returns quality score 0–100.
    Fail-safe: returns 50 on API error (goes to pending).
    """
    try:
        client = _get_client()
        prompt = f"""You are a professional blog content quality evaluator.
Rate the following blog post on a scale from 0 to 100 based on:
- Grammar and writing quality
- Informativeness and depth
- Readability and structure
- Originality and usefulness

Title: {title}
Content: {content[:3000]}

Reply with ONLY a single integer number between 0 and 100. No explanation."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5,
            temperature=0,
        )
        raw = response.choices[0].message.content.strip()
        score = int(''.join(filter(str.isdigit, raw)))
        return max(0, min(100, score))

    except Exception as e:
        logger.error(f"[Groq] Quality score check failed: {e}")
        return 50  # fail-safe → goes to pending