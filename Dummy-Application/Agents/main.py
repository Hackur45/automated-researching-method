from crewai import Crew
from agents import Agents
from tasks import Tasks
from tools import ResearcherToolSet
from dotenv import load_dotenv

def main():
    load_dotenv()

    
    print("## Welcome to the resarch paper generator ")
    print('-'*20)
    
    tasks=Tasks()
    agents_=Agents()
    
    questioning_agent=agents_.questioning_agent()
    research_agent=agents_.research_agent()
    resarch_sumarizer_agent=agents_.resarch_sumarizer_agent()
    latex_converter_agent=agents_.latex_converter_agent()
    latex_to_pdf_agent=agents_.latex_to_pdf_agent()
    
    task_question=tasks.task_question(agent=questioning_agent)
    task_resarch=tasks.task_resarch(agent=research_agent)
    format_resarch=tasks.format_resarch(agent=resarch_sumarizer_agent)
    task_convert_Latex=tasks.task_convert_Latex(agent=latex_converter_agent)
    task_convert_latex_to_pdf_and_save=tasks.task_convert_latex_to_pdf_and_save(agent=latex_to_pdf_agent)
    
    crew=Crew(
        agents=[
            questioning_agent,
            research_agent,
            resarch_sumarizer_agent,
            latex_converter_agent,
            latex_to_pdf_agent
        ],
        tasks=[
            task_question,
            task_resarch,
            format_resarch,
            task_convert_Latex,
            task_convert_latex_to_pdf_and_save
        ]
    )
    
    result= crew.kickoff()
    
    print(result)
    
if __name__=="__main__":
    main()
    