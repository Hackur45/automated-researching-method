from crewai import Agent ,Task,Crew,Process
from crewai_tools import tool
from crewai_tools.tools import FileReadTool
from crewai import LLM
import os,requests,re,mdpdf,subprocess
from dotenv import load_dotenv

load_dotenv()


class writerToolSet():
    def __init__(self):
        pass
    @tool
    def fileReadTool():
        return FileReadTool(
            file_path='template.md',
            description='A tool to read the story Template file and '
        )
    
    @tool
    def convermarkdowntopdf(markdownfile_name:str)->str:
        """
        Converts a Markdown file to a PDF document using the mdpdf command line application.

        Args:
            markdownfile_name (str): Path to the input Markdown file.

        Returns:
            str: Path to the generated PDF file.
        """

        output_file= os.path.splitext(markdownfile_name)[0]+'.pdf'
        cmd=['mdpdf','--output',output_file,markdownfile_name]

        subprocess.run(cmd,check=True)

        return output_file
    

    def 

