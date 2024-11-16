from crewai_tools import tool
from crewai_tools.tools import FileReadTool
import os,requests,re,mdpdf,subprocess
from dotenv import load_dotenv
import re
import urllib, urllib.request

load_dotenv()
class WriterToolSet:
    
    # for questioning agent 
    """ @tool
    def process_interaction(self,user_claim):
        # Store initial claim and response
        conversation_memory={
            "initial_claim":user_claim,
            "initial_response":"",
            "counter_question":[],
            "user_answers":[]
        }
        
        initial_response=self.provide_response(user_claim=user_claim)
        conversation_memory['initial_response']=initial_response
        
        for i in range(3):            
            pass
    
     """
     
    @tool
    def arxiv_resarch_tool():
        # will use arxiv api 
        
        pass 
    
    @tool
    def web_search_tool(query):
        # will use mostly crew ai tools 
        pass
    
    
     
    def resarch_tools():
        pass
     
     
     
     
    
    # for latex writer 
    @staticmethod
    @tool
    def latex_writer_tool(self,resarch_latex_code,file_name:str,output_directory):
        
        """
        Processes and writes LaTeX content to a .tex file.

        Args:
            resarch_latex (str): The LaTeX content to write into the file.
            file_name (str): The name of the research document.

        Returns:
            str: Success or error message.
        """

        # clean the name 
        file_name= re.sub(r"[^\w\s]","",file_name) 
        file_name=file_name.lower().replace(" ","_")+'.pdf'
        
        
        try:
            with open(file_name,'w') as file:
                file.write(resarch_latex_code)
        except Exception as e:
            return f"Error while creating the file: {str(e)}"
    
    # for latex  to pdf 
    def convert_latex_to_pdf(self,latex_file_name):
        """returns a pdf file with latex written 

        Args:
            latex_file_name (_type_): _description_
        """
        pass
    
    
    # for resarch storer
    @staticmethod
    @tool
    def store_pdf_to_vector_db():
        pass



    @staticmethod
    def tools():
        """
        Returns the list of tool methods that agents will use.
        """
        return [
            WriterToolSet.fileReadTool,  # Return the callable tool function
            WriterToolSet.convermarkdowntopdf  # Return the callable tool function
        ]
