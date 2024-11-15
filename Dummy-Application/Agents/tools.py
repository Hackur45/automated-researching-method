from crewai_tools import tool
from crewai_tools.tools import FileReadTool
import os,requests,re,mdpdf,subprocess
from dotenv import load_dotenv

load_dotenv()
class WriterToolSet:
    @staticmethod
    @tool
    def fileReadTool():
        """
        Reads the Story Template file and understands the expected output format.
        This tool is used to process the template file for story generation.
        """
        return FileReadTool(
            file_path='template.md',
            description='A tool to read the Story Template file and understand the expected output format.'
        )

    @staticmethod
    @tool
    def convermarkdowntopdf(markdownfile_name: str) -> str:
        """
        Converts a Markdown file to a PDF document using the mdpdf command line application.

        Args:
            markdownfile_name (str): Path to the input Markdown file.

        Returns:
            str: Path to the generated PDF file.
        """
        output_file = os.path.splitext(markdownfile_name)[0] + '.pdf'
        cmd = ['mdpdf', '--output', output_file, markdownfile_name]

        subprocess.run(cmd, check=True)

        return output_file

    @staticmethod
    def tools():
        """
        Returns the list of tool methods that agents will use.
        """
        return [
            WriterToolSet.fileReadTool,  # Return the callable tool function
            WriterToolSet.convermarkdowntopdf  # Return the callable tool function
        ]
