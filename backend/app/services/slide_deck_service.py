"""
Service for generating and refining slide decks using an LLM.
"""

import json
import logging
from typing import List, Dict, Any

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.output_parsers import JsonOutputParser
    from langchain_core.prompts import PromptTemplate
    from pydantic import BaseModel, Field
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    BaseModel = object
    # Create a fallback Field that accepts any arguments but does nothing
    def Field(*args, **kwargs):
        return None
    ChatGoogleGenerativeAI = None
    JsonOutputParser = None
    PromptTemplate = None

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Slide(BaseModel):
    """Pydantic model for a single slide's structure."""
    title: str = Field(description="The concise title of the slide.")
    content: str = Field(description="The detailed content of the slide in Markdown format. Use headings, lists, and bold text.")


class SlideDeck(BaseModel):
    """Pydantic model for the overall slide deck structure."""
    slides: List[Slide] = Field(description="A list of slide objects.")


class SlideDeckService:
    """
    A service to generate and update slide decks using LangChain and Google Gemini.
    """

    def __init__(self):
        """Initializes the Slide Deck Service."""
        self.llm = None
        self.parser = None

        if not LANGCHAIN_AVAILABLE:
            logger.warning("LangChain not installed. Slide deck generation will be disabled.")
            return

        if not settings.GOOGLE_API_KEY:
            logger.warning("GOOGLE_API_KEY not found. Slide deck generation will be disabled.")
            return

        try:
            self.parser = JsonOutputParser(pydantic_object=SlideDeck)
            self.llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0.7,
                convert_system_message_to_human=True
            )
            logger.info(f"[OK] SlideDeckService initialized with Gemini model: {settings.GEMINI_MODEL}")
        except Exception as e:
            logger.error(f"[ERROR] Failed to initialize Gemini LLM for SlideDeckService: {e}")

    async def generate_slides(
        self,
        course_name: str,
        topics: List[str],
        num_slides: int
    ) -> Dict[str, Any]:
        """Generates slide deck content based on provided topics."""
        if not self.llm:
            return {"error": "Slide deck service is not configured."}

        prompt_template = """
        You are an expert instructional designer creating a slide deck for the university course "{course_name}".

        **Requirements:**
        - **Topics to cover:** {topics}
        - **Total Number of Slides:** {num_slides}
        - **Content Style:** Clear, concise, and educational. Use Markdown for formatting (e.g., # for titles, * for lists, ** for bold).

        **Instructions:**
        1. Create a logical flow, starting with an introduction/agenda and ending with a summary.
        2. For each slide, provide a clear `title` and detailed `content` in Markdown.
        3. The content should be informative and suitable for a university-level audience.

        **Output Format:**
        You MUST provide the output as a single, valid JSON object that strictly follows this format. Do not include any other text or markdown.
        {format_instructions}
        """

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["course_name", "topics", "num_slides"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

        chain = prompt | self.llm | self.parser

        try:
            logger.info(f"Generating {num_slides} slides for course: {course_name}, topics: {topics}")
            deck_data = await chain.ainvoke({
                "course_name": course_name,
                "topics": ", ".join(topics),
                "num_slides": num_slides,
            })
            logger.info("Successfully generated slide deck content.")
            return deck_data
        except Exception as e:
            logger.error(f"Failed to generate or parse slide deck: {e}")
            return {"error": f"An error occurred while generating the slides: {str(e)}"}


slide_deck_service = SlideDeckService()
