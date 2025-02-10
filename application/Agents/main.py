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
    
    # Create agents
    questioning_agent = agents_.questioning_agent()
    research_agent = agents_.research_agent()
    research_summarizer_agent = agents_.resarch_sumarizer_agent()
    latex_converter_agent = agents_.latex_converter_agent()
    latex_to_pdf_agent = agents_.latex_to_pdf_agent()
    
    # Interactive Research Topic Collection
    initial_topic = input("Enter your research topic: ")
    
    """  task_question=tasks.task_question(agent=questioning_agent,answer='')
        task_resarch=tasks.task_resarch(agent=research_agent,user_question='',llm_answers='')
        format_resarch=tasks.format_resarch(agent=resarch_sumarizer_agent,resarch_outcomes='')
        task_convert_Latex=tasks.task_convert_Latex(agent=latex_converter_agent,resarch_name='')
        task_convert_latex_to_pdf_and_save=tasks.task_convert_latex_to_pdf_and_save(agent=latex_to_pdf_agent,latex_file_name='')
    """
    
    crew=Crew(
        agents=[
            questioning_agent,
            research_agent,
            research_summarizer_agent,
            latex_converter_agent,
            latex_to_pdf_agent
        ],
        tasks=[
            tasks.task_question(
                agent=questioning_agent,
                question=initial_topic,
                answer=""  # initally empty 
                ),
            
            tasks.task_resarch(
                agent=research_agent,
                user_question=initial_topic, #pass initial topic 
                llm_answers=""  # Will be populated dynamically 
                ),
            tasks.format_resarch(
                agent=research_summarizer_agent,
                resarch_outcomes=''# Will be populated by previous task
                ),
            # 4th Task: Convert to LaTeX
            tasks.task_convert_Latex(
                agent=latex_converter_agent,
                resarch_name=initial_topic.replace(" ", "_"),
                formated_resarch=""  # Will be populated by previous task
            ),
            
            # 5th Task: Convert LaTeX to PDF
            tasks.task_convert_latex_to_pdf_and_save(
                agent=latex_to_pdf_agent,
                latex_file_name=initial_topic.replace(" ", "_")
            )
        ],
        process="sequential",
        
    )
    
    # Execute research paper generation workflow
    result = crew.kickoff()
    
    print("\nResearch Paper Generation Complete!")
    print(result)

if __name__ == "__main__":
    main()
    