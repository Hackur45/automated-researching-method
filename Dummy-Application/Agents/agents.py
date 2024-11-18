from crewai import Agent, LLM
import os
from dotenv import load_dotenv


from tools import ResearcherToolSet

load_dotenv()


class Agents:
    def __init__(self):
        # Initialize the LLM with model and API key from environment variables
        self.llm = LLM(
            model=os.getenv("MODEL_NAME"),
            api_key=os.environ.get("GROQ_API_KEY")
        )
        
    # this agent will question  the user and take his her queries 
    def questioning_agent(self):
        return Agent(
            llm=self.llm,
            role='Questioner',
            goal="Counter-question the user based on previous answers (max 3 questions).",
            backstory="You are a researcher who analyzes questions and challenges assumptions through counter-questions.",
            allow_delegation=False,
            verbose=False
        )     
        
    # this agent will do the resarch and provide a raw format data from the web etc 
    def research_agent(self ):
        return Agent(
            llm=self.llm,
            role='Researcher',
            goal=f"Conduct thorough research on the question and summarize findings ",
            backstory="You are a researcher who performs in-depth research to provide accurate answers.",
            allow_delegation=False,
            tools=ResearcherToolSet.resarch_tools(),
            verbose=False
        )
    
    
    def resarch_sumarizer_agent(self):
        return Agent(
            llm=self.llm,
            role='Resarch Summarizer',
            goal="Convert the cluttered resarch into a summaried format which can be converted   to LaTeX code",
            backstory="You are an expert in converting cluttered resarch  into  strucutred and summarized format for research papers.",
            allow_delegation=False,
            verbose=False
        )
    
    
    # this agent will  convert the unstructured resarch of the resarch agent to a latex format and convert to pdf 
    def latex_converter_agent(self):
        return Agent(
            llm=self.llm,
            role='LaTeX Converter ',
            goal="Convert the given formated resarch to latex code and then save it to latex file",
            backstory="You are an expert in converting format resarch  into LaTeX code for research papers.",
            allow_delegation=False,
            verbose=False,
            tools=ResearcherToolSet.latex_conver_tools()
        )
    
    def latex_to_pdf_agent(self):
        return Agent(
            llm=self.llm,
            role="Latex to Pdf saver",
            goal='Given a latex file find it and convert it to a pdf using the tools provided',
            backstory='You are skilled in conveerting given latex file to a pdf file',
            allow_delegation=True,
            tools=ResearcherToolSet.latex_conver_tools()
        )
        
       
    

    
    # todo: add a agent that can store the final pdf docs to a faiss data base for a particular user so that we can add memeory to general caht bot 
    
    
