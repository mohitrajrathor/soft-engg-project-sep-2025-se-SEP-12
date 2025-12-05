# Manual Router Registration for Voice API

## Add to `backend/main.py`

After line 18 in main.py, add:
```python
from app.api import voice
```

After line 180 in main.py (after the call.router registration), add:
```python
app.include_router(voice.router, prefix=settings.API_PREFIX + "/voice", tags=["Voice Assistant"])
```

## Complete Voice Router Registration

The voice API will be available at:
- POST `/api/voice/query` - Main voice query endpoint
- GET `/api/voice/languages` - Get supported languages
- POST `/api/voice/test-tts` - Test TTS functionality

This enables the multilingual voice assistant feature!
