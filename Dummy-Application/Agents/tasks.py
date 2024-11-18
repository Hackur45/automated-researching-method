from crewai import  Task


class Tasks:
    def task_question(self, agent,question,answer):
        return Task(
            description=f"given a question :{question} and a answer:{answer} genrate a counter question",
            expected_output="A counter question which either supports, opposes or explores the idea provided ",
            agent=agent
        )

    def task_resarch(self, agent,user_question: str,llm_answers:str):
        return Task(
            description=f"Based on the userquestions :{user_question} and the llm answers:{llm_answers} you have to do a through resarch ",
            agent=agent,
            expected_output="A text output which has throughly resarched the topic in depth like if you were the best in it ",
        )

    def format_resarch(self, agent,resarch_outcomes):
        return Task(
            description=f"Given a resarch insights summarize it in a way that caan be latex compaatible to build a resarch paper of minimum 4 pages:{resarch_outcomes}",
            agent=agent,
            expected_output="A proper summarized latex comptible resarch paper ready formated text and also provide the resarch a name"
        )

    def task_convert_Latex(self, agent,formated_resarch,resarch_name):
        return Task(
            description=f"Convert the  latex compatible resarch outcomes to latex code and save it to a .tex file.:{formated_resarch} and give it a name {resarch_name}.tex",
            agent=agent,
            expected_output="A latex code of the resarch outcome in proper research paper formmat and also a name to it ",
            output_file=f"output/{resarch_name}.tex"
        )
    
    def task_convert_latex_to_pdf_and_save(self,agent,latex_file_name):
        return Task(
            description=f'Convert a given latex file to pdf and save it user directory:{latex_file_name}',
            agent=agent,
            expected_output=f"A pdf file with compiled latex code in it as a research paper",
            output_file=f"output/{latex_file_name}.pdf" 
        )
        
    # todo : add task to store papers in faiss