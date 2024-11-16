from crewai import LLM, Task


class Tasks:
    def task_question(self, agent,question,answer):
        return Task(
            description=f"given a question :{question} and a answer:{answer} genrate a counter question",
            expected_output="A counter question which either supports, opposes or explore the idea provided ",
            agent=agent
        )

    def task_resarch(self, agent,):
        return Task(
            description="Using the outline provided, write the full story content for all chapters, ensuring a cohesive and engaging narrative for children. Each Chapter 100 words. Include Title of the story at the top.",
            agent=agent,
            expected_output="A complete manuscript of the children's storybook about Animals with 5 chapters. Each chapter should contain approximately 100 words, following the provided outline and integrating the characters and plot points into a cohesive narrative.",
        )

    """  def task_convert_(self, agent, context=None):
            return Task(
                description="Format the story content in markdown, including an image at the beginning of each chapter.",
                agent=agent,
                expected_output="The entire storybook content formatted in markdown, with each chapter title followed by the corresponding image and the chapter content.",
                context=context,
                output_file="story.md",
            )
    """
    def task_convert_Latex(self, agent):
        return Task(
            description="Convert a Markdown file to a PDF document, ensuring the preservation of formatting, structure, and embedded images using the mdpdf library.",
            agent=agent,
            expected_output="A PDF file generated from the Markdown input, accurately reflecting the content with proper formatting. The PDF should be ready for sharing or printing.",
        )
    
    def task_convert_latex_to_pdf(self,agent):
        return Task(
            description='',
            agent=agent,
            expected_output=""
            
        )
        
    # todo : add task to store papers in faiss