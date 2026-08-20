from typing import Dict, Any, List

# Regional Language Registry covering 15 Indian languages
INDIAN_LANGUAGES_REGISTRY = {
    "hi": {"name": "Hindi", "stt_supported": True, "tts_supported": True},
    "kn": {"name": "Kannada", "stt_supported": True, "tts_supported": True},
    "te": {"name": "Telugu", "stt_supported": True, "tts_supported": True},
    "ta": {"name": "Tamil", "stt_supported": True, "tts_supported": True},
    "ml": {"name": "Malayalam", "stt_supported": True, "tts_supported": True},
    "mr": {"name": "Marathi", "stt_supported": True, "tts_supported": True},
    "bn": {"name": "Bengali", "stt_supported": True, "tts_supported": True},
    "gu": {"name": "Gujarati", "stt_supported": True, "tts_supported": True},
    "pa": {"name": "Punjabi", "stt_supported": True, "tts_supported": True},
    "or": {"name": "Odia", "stt_supported": True, "tts_supported": True},
    "as": {"name": "Assamese", "stt_supported": True, "tts_supported": True},
    "ur": {"name": "Urdu", "stt_supported": True, "tts_supported": True},
    "mai": {"name": "Maithili", "stt_supported": False, "tts_supported": False},
    "kok": {"name": "Konkani", "stt_supported": False, "tts_supported": False},
    "ks": {"name": "Kashmiri", "stt_supported": False, "tts_supported": False},
}

class MultilingualVoiceEngine:
    """Multilingual & Speech Processing Engine abstraction."""
    def get_supported_languages(self) -> List[Dict[str, Any]]:
        return [
            {"code": code, "name": meta["name"], "voice_enabled": meta["stt_supported"]}
            for code, meta in INDIAN_LANGUAGES_REGISTRY.items()
        ]

    def translate_and_process(self, input_text: str, target_lang: str = "hi") -> Dict[str, Any]:
        lang_info = INDIAN_LANGUAGES_REGISTRY.get(target_lang, INDIAN_LANGUAGES_REGISTRY["hi"])
        return {
            "original_text": input_text,
            "target_language": lang_info["name"],
            "translated_text": input_text, # Keeps English text or translated text based on provider
            "stt_status": "Active" if lang_info["stt_supported"] else "Fallback text mode"
        }

multilingual_engine = MultilingualVoiceEngine()
