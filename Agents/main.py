from crewai import Agent ,Task,Crew,Process
from crewai_tools import tool
from crewai_tools.tools import FileReadTool
from crewai import LLM

from dotenv import load_dotenv
from crewai import Crew
from tasks import Tasks
from agents import Agents


def main():
    load_dotenv()
    
    print("hello welcome")
    
    tasks=Tasks()
    agents=Agents()
    
    



crew = Crew(
  agents=[story_outliner, story_writer, image_generator, content_formatter, markdown_to_pdf_creator],
  tasks=[task_outline, task_write, task_image_generate, task_format_content, task_markdown_to_pdf],
  verbose=True,
  process=Process.sequential
)

result = crew.kickoff()

print(result