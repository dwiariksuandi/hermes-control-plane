"""Aegis Cognitive Shield — PII/Secret redaction and prompt injection detection."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv("/home/hiryu/.hermes/.env")

def redact_secrets(text: str) -> str:
    """Detect and redact PII and secrets using Presidio."""
    try:
        from presidio_analyzer import AnalyzerEngine
        from presidio_anonymizer import AnonymizerEngine
    except ImportError:
        return text

    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()
    results = analyzer.analyze(text=text, language='en')
    redacted = anonymizer.anonymize(text=text, analyzer_results=results)
    return redacted.text

def detect_injection(text: str) -> bool:
    """Detect prompt injection using Rebuff."""
    try:
        from rebuff import RebuffSdk
    except ImportError:
        return False

    api_key = os.environ.get("OPENAI_API_KEY")
    pinecone_key = os.environ.get("PINECONE_API_KEY")
    pinecone_index = os.environ.get("PINECONE_INDEX")

    if not (api_key and pinecone_key and pinecone_index):
        import logging
        logging.getLogger("aegis_cognitive").warning("Rebuff credentials missing. Prompt injection detection DISABLED.")
        return False

    try:
        rb = RebuffSdk(api_key, pinecone_key, pinecone_index)
        result = rb.detect_injection(text)
        return result.injection_detected
    except Exception:
        return False

def sanitize_input(text: str) -> str:
    """Master sanitization: redact then injection check."""
    sanitized = redact_secrets(text)
    if detect_injection(sanitized):
        return "[PROMPT_INJECTION_DETECTED_AND_REMOVED]"
    return sanitized
