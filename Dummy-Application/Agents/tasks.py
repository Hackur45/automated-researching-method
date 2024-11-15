from crewai import LLM, Task


class Tasks:
    def task_outline(self, agent):
        return Task(
            description="Create an outline for the children's storybook about Animals, detailing chapter titles and character descriptions for 5 chapters.",
            agent=agent,
            expected_output="A structured outline document containing 5 chapter titles, with detailed character descriptions and the main plot points for each chapter.",
        )

    def task_write(self, agent):
        return Task(
            description="Using the outline provided, write the full story content for all chapters, ensuring a cohesive and engaging narrative for children. Each Chapter 100 words. Include Title of the story at the top.",
            agent=agent,
            expected_output="A complete manuscript of the children's storybook about Animals with 5 chapters. Each chapter should contain approximately 100 words, following the provided outline and integrating the characters and plot points into a cohesive narrative.",
        )

    def task_format_content(self, agent, context=None):
        return Task(
            description="Format the story content in markdown, including an image at the beginning of each chapter.",
            agent=agent,
            expected_output="The entire storybook content formatted in markdown, with each chapter title followed by the corresponding image and the chapter content.",
            context=context,
            output_file="story.md",
        )

    def task_markdown_to_pdf(self, agent):
        return Task(
            description="Convert a Markdown file to a PDF document, ensuring the preservation of formatting, structure, and embedded images using the mdpdf library.",
            agent=agent,
            expected_output="A PDF file generated from the Markdown input, accurately reflecting the content with proper formatting. The PDF should be ready for sharing or printing.",
        )
