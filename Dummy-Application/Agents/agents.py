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
    
    """ def questioning_agent(self):
        return Agent(
            llm=self.llm,
            role='Questioner',
            goal="Counter-question the user based on previous answers (max 3 questions).",
            backstory="You are a researcher who analyzes questions and challenges assumptions through counter-questions.",
      
            allow_delegation=False,
            verbose=False
        ) """
    
    def research_agent(self, user_question: str):
        return Agent(
            llm=self.llm,
            role='Researcher',
            goal=f"Conduct thorough research on the question and summarize findings: '{user_question}' ",
            backstory="You are a researcher who performs in-depth research to provide accurate answers.",
            allow_delegation=False,
            tools='',
            verbose=False
        )
    
    def convert_md_agent(self, research_output: str):
        return Agent(
            llm=self.llm,
            role='Mark Down  Formatter',
            goal=f"Format the research output  to markdown : '{research_output}' ",
            backstory="You are a markdown  formatter specialized in converting research content into markdown format.",
            allow_delegation=False,
            tools='',
            verbose=False
        )
    
    def latex_converter_agent(self, markdown_file_name: str):
        return Agent(
            llm=self.llm,
            role='LaTeX Converter',
            goal="Convert the markdown  to LaTeX code",
            backstory="You are an expert in converting markdown into LaTeX code for research papers.",
            allow_delegation=False,
            verbose=False,
            tools=''
        )
    
    # todo: add a agent that can store the final pdf docs to a faiss data base for a particular user so that we can add memeory to general caht bot 
    
    
