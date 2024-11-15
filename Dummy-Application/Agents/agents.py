from crewai import Agent, LLM
from tools import WriterToolSet
import os
from dotenv import load_dotenv


load_dotenv()


class Agents:
    def __init__(self):
        # Initialize the LLM with model and API key from environment variables
        self.llm = LLM(
            model=os.getenv("MODEL_NAME"),
            api_key=os.environ.get("GROQ_API_KEY")
        )
    
    def questioning_agent(self):
        return Agent(
            llm=self.llm,
            role='Questioner',
            goal="Counter-question the user based on previous answers (max 3 questions).",
            backstory="You are a researcher who analyzes questions and challenges assumptions through counter-questions.",
            allow_delegation=False,
            verbose=False
        )
    
    def research_agent(self, user_question: str):
        return Agent(
            llm=self.llm,
            role='Researcher',
            goal=f"Conduct thorough research on the question: '{user_question}' and summarize findings.",
            backstory="You are a researcher who performs in-depth research to provide accurate answers.",
            allow_delegation=False,
            verbose=False
        )
    
    def formater_agent(self, research_output: str):
        return Agent(
            llm=self.llm,
            role='Text Formatter',
            goal=f"Format the research output: '{research_output}' to be LaTeX compatible.",
            backstory="You are a text formatter specialized in converting research content into LaTeX-compatible format.",
            allow_delegation=False,
            verbose=False
        )
    
    def latex_converter_agent(self, formatted_text: str):
        return Agent(
            llm=self.llm,
            role='LaTeX Converter',
            goal=f"Convert the formatted text to LaTeX code: '{formatted_text}'",
            backstory="You are an expert in converting text into LaTeX code for research papers.",
            allow_delegation=False,
            verbose=False
        )
    
    # todo: add a agent that can store the final pdf docs to a fiass data base for a particular user so that we can add memeory to general caht bot 
    
    