from crewai import Agent, LLM
from tools import WriterToolSet
import os

class Agents:
    def __init__(self):
        # Initialize the LLM with model and API key from environment variables
        self.llm = LLM(
            model="groq/llama3-8b-8192", 
            api_key=os.environ.get("GROQ_API_KEY")
        )

    def story_outliner_agent(self):
        return Agent(
            llm=self.llm,
            role="Story Outliner",
            goal="Develop an outline for a children's storybook about Animals, including chapter titles and characters for 5 chapters.",
            backstory="An imaginative creator who lays the foundation of captivating stories for children.",
            allow_delegation=False,
            verbose=True,
        )

    def story_writer_agent(self):
        return Agent(
            role="Story Writer",
            goal="Write the full content of the story for all 5 chapters, each chapter 100 words, weaving together the narratives and characters outlined.",
            backstory="A talented storyteller who brings to life the world and characters outlined, crafting engaging and imaginative tales for children.",
            verbose=True,
            llm=self.llm,
            allow_delegation=False,
        )

    def content_formater_agent(self):
        return Agent(
            role="Content Formatter",
            goal="Format the written story content in markdown, including images at the beginning of each chapter.",
            backstory="A meticulous formatter who enhances the readability and presentation of the storybook.",
            verbose=True,
            llm=self.llm,
            tools=WriterToolSet.tools(),  # Assuming WriterToolSet.tools() returns correct tool functions
            allow_delegation=False,
        )

    def markdown_to_pdf_creator_agent(self):
        return Agent(
            role="PDF Converter",
            goal="Convert the Markdown file to a PDF document. story.md is the markdown file name.",
            backstory="An efficient converter that transforms Markdown files into professionally formatted PDF documents.",
            verbose=True,
            llm=self.llm,
            tools=WriterToolSet.tools(),  # Ensure tools are correct here
            allow_delegation=False,
        )
