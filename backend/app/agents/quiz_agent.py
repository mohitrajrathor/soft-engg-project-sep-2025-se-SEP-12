# quiz agent module

# imports
from langchain_google_genai import ChatGoogleGenerativeAI
from app.schemas.quiz import Question, QuizContent, QuizResponse
from app.agents.prompts import build_quiz_prompt, build_update_quiz_prompt
import json
import re



class QuizGenAgent:
    def __init__(self, llm: ChatGoogleGenerativeAI) -> None:
        """ 
        Agent to create and update quizzez
        args:
            llm : ChatGoogleGenerativeAI intance

        return: 
            None
        """
        self.llm = llm

    def _extract_response(self, text: str) -> QuizResponse:
        """Extract json from llm response and convert it to QuizResponse object"""
        try:
            json_str = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL).group(1)
            data = json.loads(json_str)
            response = QuizResponse(**data)
            return response
        except Exception as e:
            raise e


    def generate(self, user_query: str) -> QuizResponse:
        """ 
        Generate Quiz based on given query.
        """
        try:
            prompt = build_quiz_prompt(user_query)
            llm_response = self.llm.invoke(prompt)
            

            quiz_obj = self._extract_response(str(llm_response.content))

            return quiz_obj
        
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response from LLM: {e}")
        
    
    def update(self, quiz: QuizContent, feedback: str) -> QuizResponse:
        """ 
        Update an existing quiz based on user feedback.
        """
        try:
            prompt = build_update_quiz_prompt(quiz, feedback)
            llm_res = self.llm.invoke(prompt)
            
            quiz_obj = self._extract_response(llm_res.content)
            return quiz_obj

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response from LLM: {e}")

