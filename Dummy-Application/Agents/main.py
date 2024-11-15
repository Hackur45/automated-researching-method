#import just the titles
from crewai import Crew,Process
from dotenv import load_dotenv

from tasks import Tasks
from agents import Agents



def main():
  
    load_dotenv()
  
    print("hello welcome")
  
    tasks=Tasks()
  
    agents=Agents()    
    
    
    story_outliner_agent=agents.story_outliner_agent()
    story_writer_agent=agents.story_writer_agent()
    content_formater_agent=agents.content_formater_agent()
    markdown_to_pdf_creator_agent=agents.markdown_to_pdf_creator_agent()
     
    task_outline=tasks.task_outline(story_outliner_agent)
    task_write=tasks.task_write(story_writer_agent)
    task_format_content = tasks.task_format_content(
        content_formater_agent, 
        context=[task_write]  # Pass the task reference, not method call
    )
    task_markdown_to_pdf=tasks.task_markdown_to_pdf(markdown_to_pdf_creator_agent)
    

    crew = Crew(
      agents=[story_outliner_agent, story_writer_agent, content_formater_agent, markdown_to_pdf_creator_agent],
      tasks=[task_outline, task_write, task_format_content, task_markdown_to_pdf],
      verbose=True,
      process=Process.sequential
    )
    result = crew.kickoff()
    print(result)
    
    
    
if __name__ == "__main__":
    main()
