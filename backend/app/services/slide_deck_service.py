"""
Service for generating and refining slide decks using an LLM.
"""

import json
import logging
import random
from typing import List, Dict, Any, Optional
from enum import Enum

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
from app.services.chart_generator import chart_generator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphType(str, Enum):
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    SCATTER = "scatter"


class GraphData(BaseModel):
    type: GraphType
    title: str
    labels: List[str]
    datasets: List[Dict[str, Any]]


class Slide(BaseModel):
    """Pydantic model for a single slide's structure."""
    title: str = Field(description="The concise title of the slide.")
    content: str = Field(description="The detailed content of the slide in Markdown format. Use headings, lists, and bold text.")
    graph_data: Optional[GraphData] = Field(None, description="Optional graph data for the slide.")
    graph_image: Optional[str] = Field(None, description="Optional base64 Data URI of chart image (PNG).")


class SlideDeck(BaseModel):
    """Pydantic model for the overall slide deck structure."""
    slides: List[Slide] = Field(description="A list of slide objects.")


class SlideDeckPreview(BaseModel):
    """Preview of the slide deck."""
    outline: List[str] = Field(description="Bullet points outlining the slide deck content.")


class SlideDeckService:
    """
    A service to generate and update slide decks using LangChain and Google Gemini.
    """

    def __init__(self):
        """Initializes the Slide Deck Service."""
        self.llm = None
        self.parser = None
        self.preview_parser = None

        if not LANGCHAIN_AVAILABLE:
            logger.warning("LangChain not installed. Slide deck generation will be disabled.")
            return

        if not settings.GOOGLE_API_KEY:
            logger.warning("GOOGLE_API_KEY not found. Slide deck generation will be disabled.")
            return

        try:
            self.parser = JsonOutputParser(pydantic_object=SlideDeck)
            self.preview_parser = JsonOutputParser(pydantic_object=SlideDeckPreview)
            self.llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0.7,
                convert_system_message_to_human=True
            )
            logger.info(f"[OK] SlideDeckService initialized with Gemini model: {settings.GEMINI_MODEL}")
        except Exception as e:
            logger.error(f"[ERROR] Failed to initialize Gemini LLM for SlideDeckService: {e}")

    async def generate_preview(
        self,
        course_name: str,
        topics: List[str],
        num_slides: int,
        description: str,
        format: str
    ) -> Dict[str, Any]:
        """Generates a preview outline of the slide deck."""
        if not self.llm:
            return {"error": "Slide deck service is not configured."}

        prompt_template = """
        You are an expert instructional designer creating a slide deck outline for the university course "{course_name}".

        **Requirements:**
        - **Topics to cover:** {topics}
        - **Total Number of Slides:** {num_slides}
        - **Description:** {description}
        - **Format:** {format} (presentation: concise, bullet points; document: detailed paragraphs)

        **Instructions:**
        Provide a high-level outline as a list of bullet points describing what each slide will contain.

        **Output Format:**
        You MUST provide the output as a single, valid JSON object with an "outline" array of strings.
        {format_instructions}
        """

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["course_name", "topics", "num_slides", "description", "format"],
            partial_variables={"format_instructions": self.preview_parser.get_format_instructions()}
        )

        chain = prompt | self.llm | self.preview_parser

        try:
            logger.info(f"Generating preview for {num_slides} slides for course: {course_name}")
            preview_data = await chain.ainvoke({
                "course_name": course_name,
                "topics": ", ".join(topics),
                "num_slides": num_slides,
                "description": description,
                "format": format,
            })
            logger.info("Successfully generated slide deck preview.")
            return preview_data
        except Exception as e:
            logger.error(f"Failed to generate preview: {e}")
            return {"error": f"An error occurred while generating the preview: {str(e)}"}

    async def generate_slides(
        self,
        course_name: str,
        topics: List[str],
        num_slides: int,
        description: str,
        format: str,
        include_graphs: bool,
        graph_types: Optional[List[GraphType]]
    ) -> Dict[str, Any]:
        """Generates slide deck content based on provided topics."""
        if not self.llm:
            return {"error": "Slide deck service is not configured."}

        content_length = "concise bullet points and short paragraphs" if format == "presentation" else "detailed explanations and longer content"

        graph_instruction = ""
        if include_graphs and graph_types:
            graph_instruction = f"""
        - **Include Graphs:** For relevant slides, include graph_data with one of the types: {', '.join([gt.value for gt in graph_types])}.
          Generate appropriate data for the graph based on the slide content.
        """

        prompt_template = """
        You are an expert instructional designer creating a slide deck for the university course "{course_name}".

        **Requirements:**
        - **Topics to cover:** {topics}
        - **Total Number of Slides:** {num_slides}
        - **Description:** {description}
        - **Format:** {format}
        - **Content Length:** {content_length}
        {graph_instruction}

        **Instructions:**
        1. Create a logical flow, starting with an introduction/agenda and ending with a summary.
        2. For each slide, provide a clear `title` and `content` in Markdown.
        3. The content should be informative and suitable for a university-level audience.
        4. If graphs are included, add `graph_data` for appropriate slides.

        **Output Format:**
        You MUST provide the output as a single, valid JSON object that strictly follows this format. Do not include any other text or markdown.
        {format_instructions}
        """

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["course_name", "topics", "num_slides", "description", "format", "content_length", "graph_instruction"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

        chain = prompt | self.llm | self.parser

        try:
            logger.info(f"Generating {num_slides} slides for course: {course_name}, topics: {topics}")
            deck_data = await chain.ainvoke({
                "course_name": course_name,
                "topics": ", ".join(topics),
                "num_slides": num_slides,
                "description": description,
                "format": format,
                "content_length": content_length,
                "graph_instruction": graph_instruction,
            })
            
            # Post-process: Add charts to appropriate slides
            if include_graphs and graph_types and "slides" in deck_data:
                slides = deck_data["slides"]
                deck_data["slides"] = self._add_charts_to_slides(
                    slides, 
                    graph_types, 
                    course_name
                )
            
            logger.info("Successfully generated slide deck content.")
            return deck_data
        except Exception as e:
            logger.error(f"Failed to generate or parse slide deck: {e}")
            return {"error": f"An error occurred while generating the slides: {str(e)}"}
    
    def _add_charts_to_slides(
        self, 
        slides: List[Dict[str, Any]], 
        graph_types: List[GraphType],
        course_name: str
    ) -> List[Dict[str, Any]]:
        """
        Add chart images to slides that would benefit from visualization.
        
        Args:
            slides: List of slide dictionaries
            graph_types: Preferred chart types
            course_name: Course name for context
        
        Returns:
            Updated slides with graph_image and graph_data fields
        """
        # Skip first (intro) and last (summary) slides
        content_slides = slides[1:-1] if len(slides) > 2 else slides
        
        # Determine which slides should get charts (30-50% of content slides)
        num_charts = max(1, min(len(content_slides) // 2, 3))
        
        # Select slides for charts (prefer those with keywords)
        chart_keywords = ['data', 'trend', 'growth', 'comparison', 'analysis', 'performance', 
                         'statistics', 'metrics', 'results', 'distribution']
        
        scored_slides = []
        for idx, slide in enumerate(content_slides):
            title = slide.get('title', '').lower()
            content = slide.get('content', '').lower()
            score = sum(1 for kw in chart_keywords if kw in title or kw in content)
            scored_slides.append((score, idx, slide))
        
        # Sort by score and select top candidates
        scored_slides.sort(reverse=True, key=lambda x: x[0])
        selected_indices = [idx for _, idx, _ in scored_slides[:num_charts]]
        
        # Generate charts for selected slides
        for slide_idx in selected_indices:
            slide = content_slides[slide_idx]
            slide_title = slide.get('title', '')
            
            # Choose chart type (cycle through available types)
            chart_type = graph_types[slide_idx % len(graph_types)].value
            
            # Generate synthetic data
            labels, values = chart_generator.generate_synthetic_data(
                slide_title=slide_title,
                chart_type=chart_type,
                slide_index=slide_idx
            )
            
            # Generate chart image
            chart_title = f"{slide_title} - Visualization"
            graph_image = chart_generator.generate_chart_image(
                chart_type=chart_type,
                title=chart_title,
                labels=labels,
                values=values,
                slide_title=slide_title,
                slide_index=slide_idx
            )
            
            if graph_image:
                # Add both graph_image (for rendering) and graph_data (for metadata)
                slide['graph_image'] = graph_image
                
                # Format graph_data for compatibility
                if chart_type == "scatter" and values and isinstance(values[0], (list, tuple)):
                    # For scatter, extract x and y separately
                    x_vals, y_vals = zip(*values)
                    datasets = [
                        {"label": "Data Points", "data": list(y_vals)}
                    ]
                    labels_list = [f"Point {i+1}" for i in range(len(x_vals))]
                else:
                    datasets = [{"label": "Values", "data": values}]
                    labels_list = labels
                
                slide['graph_data'] = {
                    "type": chart_type,
                    "title": chart_title,
                    "labels": labels_list,
                    "datasets": datasets
                }
                
                logger.info(f"Added {chart_type} chart to slide: {slide_title}")
        
        return slides


slide_deck_service = SlideDeckService()
