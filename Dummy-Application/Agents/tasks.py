from crewai import  Task

class Tasks:
    # In tasks.py
    def task_question(self, agent, question, answer):
        return Task(
            description=f"Generate insightful counter-questions about: {question}",
            expected_output="""A structured response with:
    1. A thought process explaining the approach
    2. Specific, probing questions that explore different research angles
    3. A clear, concise final answer""",
            agent=agent,
            # Add more specific instructions
            context_description=f"Original Topic: {question}. Provide questions that reveal deeper research dimensions."
        )
        
    def task_resarch(self, agent, user_question, llm_answers):
        return Task(
            description=f"Conduct comprehensive research on: {user_question} "
                        f"considering previous insights: {llm_answers}",
            expected_output="Detailed research findings covering multiple perspectives",
            agent=agent,
            # Add context output key
            output_key='research_output'
        )

    def format_resarch(self, agent, resarch_outcomes):
        return Task(
            description=f"Synthesize research into a structured academic format: {resarch_outcomes}",
            expected_output="Academic-style research summary suitable for LaTeX conversion",
            agent=agent,
            # Add context output key
            output_key='formatted_research'
        )

    def task_convert_Latex(self, agent,formated_resarch:str,resarch_name:str):
        return Task(
            description=f"Convert the  latex compatible resarch outcomes to latex code and save it to a .tex file.:{formated_resarch} and give it a name {resarch_name}.tex",
            agent=agent,
            expected_output="A latex code of the resarch outcome in proper research paper formmat and also a name to it ",
            output_file=f"output/{resarch_name}.tex"
        )
    
    def task_convert_latex_to_pdf_and_save(self,agent,latex_file_name:str):
        return Task(
            description=f'Convert a given latex file to pdf and save it user directory:{latex_file_name}',
            agent=agent,
            expected_output=f"A pdf file with compiled latex code in it as a research paper",
            output_file=f"output/{latex_file_name}.pdf" 
        )
        
    # todo : add task to store papers in faiss