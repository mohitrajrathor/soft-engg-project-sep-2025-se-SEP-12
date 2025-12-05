"""
Voice Chat API

Endpoints for voice-based chatbot interaction
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
import logging
import os
import tempfile

from app.core.db import get_db
from app.utils.audio_processor import (
    transcribe_audio,
    text_to_speech,
    save_temp_audio,
    validate_audio_file,
    get_supported_languages
)
from app.models.chat import Chat, RAGQuery
from app.pipelines.chat import process_query
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()

# Maximum audio file size (10 MB)
MAX_AUDIO_SIZE = 10 * 1024 * 1024


@router.post("/query")
async def voice_query(
    audio: UploadFile = File(...),
    chat_id: Optional[str] = Form(None),
    language: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Process voice query through RAG chatbot.
    
    Flow:
    1. Receive audio file
    2. Transcribe with Whisper → text + detected language
    3. Process through existing RAG pipeline
    4. Convert answer to speech with gTTS
    5. Return audio response + metadata
    
    Args:
        audio: Audio file (MP3, WAV, WebM, etc.)
        chat_id: Optional chat session ID for conversation continuity
        language: Optional language hint (for better STT accuracy)
        
    Returns:
        JSON with audio_url, transcript, answer_text, detected_language
    """
    temp_audio_path = None
    temp_response_path = None
    
    try:
        # Read audio file
        audio_content = await audio.read()
        
        # Validate audio
        validate_audio_file(audio_content, max_size_mb=10)
        
        logger.info(f"Received voice query: {len(audio_content)} bytes, chat_id={chat_id}")
        
        # Save to temporary file for Whisper
        temp_audio_path = save_temp_audio(audio_content, suffix='.mp3')
        
        # Step 1: Transcribe audio → text
        try:
            transcript, detected_lang = transcribe_audio(temp_audio_path, language=language)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Could not understand audio. Please speak clearly and try again. Error: {str(e)}"
            )
        
        if not transcript or len(transcript.strip()) < 3:
            raise HTTPException(
                status_code=400,
                detail="No speech detected in audio. Please speak louder or closer to the microphone."
            )
        
        logger.info(f"Transcribed: '{transcript}' (language: {detected_lang})")
        
        # Step 2: Get or create chat session
        if chat_id:
            chat = db.query(Chat).filter(Chat.id == chat_id).first()
            if not chat:
                # Create new chat with provided ID
                chat = Chat(id=uuid.UUID(chat_id))
                db.add(chat)
                db.commit()
        else:
            # Create new chat session
            chat = Chat()
            db.add(chat)
            db.commit()
            chat_id = str(chat.id)
        
        # Step 3: Process through existing RAG pipeline
        try:
            result = process_query(
                input_text=transcript,
                chat_id=chat_id,
                db=db
            )
            
            answer_text = result.get('answer', '')
            confidence = result.get('confidence', 0)
            sources = result.get('sources', [])
            
        except Exception as e:
            logger.error(f"RAG processing failed: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to process query: {str(e)}"
            )
        
        if not answer_text:
            answer_text = "I apologize, but I couldn't find an answer to your question. Could you please rephrase or ask something else?"
        
        logger.info(f"Generated answer: '{answer_text[:100]}...'")
        
        # Step 4: Convert answer to speech
        try:
            # Use detected language for TTS
            audio_response_bytes = text_to_speech(answer_text, language=detected_lang)
        except Exception as e:
            logger.error(f"TTS failed: {str(e)}, falling back to English")
            # Fallback to English if TTS fails for detected language
            try:
                audio_response_bytes = text_to_speech(answer_text, language='en')
                detected_lang = 'en'
            except Exception as e2:
                raise HTTPException(
                    status_code=500,
                    detail=f"Text-to-speech failed: {str(e2)}"
                )
        
        # Step 5: Return response
        # Return audio as streaming response
        return StreamingResponse(
            iter([audio_response_bytes]),
            media_type="audio/mpeg",
            headers={
                "X-Chat-ID": chat_id,
                "X-Transcript": transcript,
                "X-Answer": answer_text,
                "X-Language": detected_lang,
                "X-Confidence": str(confidence),
                "Content-Disposition": f"attachment; filename=response.mp3"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Voice query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup temporary files
        if temp_audio_path and os.path.exists(temp_audio_path):
            try:
                os.unlink(temp_audio_path)
            except:
                pass


@router.get("/languages")
async def get_languages():
    """
    Get list of supported languages for TTS.
    
    Returns:
        Dict of language codes and names
    """
    return {
        "languages": get_supported_languages(),
        "whisper_note": "Whisper STT supports 99 languages with auto-detection"
    }


@router.post("/test-tts")
async def test_tts(
    text: str = Form(...),
    language: str = Form('en')
):
    """
    Test endpoint for TTS functionality.
    
    Args:
        text: Text to convert to speech
        language: Language code (default: 'en')
        
    Returns:
        Audio file (MP3)
    """
    try:
        audio_bytes = text_to_speech(text, language=language)
        
        return StreamingResponse(
            iter([audio_bytes]),
            media_type="audio/mpeg",
            headers={"Content-Disposition": f"attachment; filename=test_tts.mp3"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
