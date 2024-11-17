from crewai_tools import tool, RagTool
from crewai_tools.tools import FileReadTool
import os, requests, re, mdpdf, subprocess
from dotenv import load_dotenv
import re
import urllib.request as libreq
from bs4 import BeautifulSoup
from urllib.parse import quote

load_dotenv()


class WriterToolSet:

    # for questioning agent
    """@tool
    def process_interaction(self,user_claim):
        # Store initial claim and response
        conversation_memory={
            "initial_claim":user_claim,
            "initial_response":"",
            "counter_question":[],
            "user_answers":[]
        }

        initial_response=self.provide_response(user_claim=user_claim)
        conversation_memory['initial_response']=initial_response

        for i in range(3):
            pass

    """

    # resarcher tools
    @tool
    def arxiv_research_tool(
        author, title, category, sortBy, maxResults=1, sortOrder="ascending"
    ):
        """_summary_

        Args:
            author (_type_): _description_
            title (_type_): _description_
            category (_type_): _description_
            sortBy (_type_): _description_
            maxResults (int, optional): _description_. Defaults to 1.
            sortOrder (str, optional): _description_. Defaults to "ascending".

        Returns:
            _type_: _description_
        """


        # 1. Input validation
        if not any([author, title, category]):
            return "Error: At least one search parameter (author, title, or category) must be provided"

        # 2. Build search query more flexibly
        # quote is used to add http safe searches
        search_parts = []
        if author:
            search_parts.append(f"au:{quote(author)}")
        if title:
            search_parts.append(f"ti:{quote(title)}")
        if category:
            search_parts.append(f"cat:{quote(category)}")

        search_query = "+AND+".join(search_parts)

        # 3. Validate maxResults
        maxResults = min(max(1, maxResults), 4)

        # 4. Validate sortOrder
        valid_sort_orders = ["ascending", "descending"]
        sortOrder = (
            sortOrder.lower() if sortOrder.lower() in valid_sort_orders else "ascending"
        )

        # 5. Validate sortBy
        valid_sort_by = ["relevance", "lastUpdatedDate", "submittedDate"]

        if sortBy not in valid_sort_by:
            sortBy = "relevance"

        try:
            base_url = "http://export.arxiv.org/api/query"
            params = {
                "search_query": search_query,
                "max_results": maxResults,
                "sortBy": sortBy,
                "sortOrder": sortOrder,
            }

            url = f"{base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"

            # 7. Make request with timeout
            with libreq.urlopen(url, timeout=10) as response:
                xml_data = response.read().decode("utf-8")

                # 8. Parse XML
                soup = BeautifulSoup(xml_data, "xml")
                entries = soup.find_all("entry")
                data = []
                for entry in entries:
                    entry_data = {
                        "summary": (
                            entry.find("summary").text.strip()
                            if entry.find("summary")
                            else None
                        ),
                        "link": (
                            entry.find("link", title="pdf")["href"]
                            if entry.find("link", title="pdf")
                            else None
                        ),
                    }
                    data.append(entry_data)

            return data
        except Exception as e:
            return f"Error occurred: {str(e)}"

    @tool
    def web_search_tool(query):
        """_summary_

        Args:
            query (_type_): _description_
        """
        # will use mostly crew ai tools
        pass

    # for latex writer
    @staticmethod
    @tool
    def latex_writer_tool(self, resarch_latex_code, file_name: str, output_directory):
        """
        Processes and writes LaTeX content to a .tex file.

        Args:
            resarch_latex (str): The LaTeX content to write into the file.
            file_name (str): The name of the research document.

        Returns:
            str: Success or error message.
        """

        # clean the name
        file_name = re.sub(r"[^\w\s]", "", file_name)
        file_name = file_name.lower().replace(" ", "_") + ".pdf"

        try:
            with open(file_name, "w") as file:
                file.write(resarch_latex_code)
        except Exception as e:
            return f"Error while creating the file: {str(e)}"

    # for latex  to pdf
    def convert_latex_to_pdf(self, latex_file_name):
        """returns a pdf file with latex written

        Args:
            latex_file_name (_type_): _description_
        """
        pass

    # for resarch storer
    @staticmethod
    @tool
    def store_pdf_to_vector_db():
        """_summary_
        """
        pass

    @staticmethod
    def tools():
        """_summary_

        Returns:
            _type_: _description_
        """
        return [
            WriterToolSet.fileReadTool,  # Return the callable tool function
            WriterToolSet.convermarkdowntopdf,  # Return the callable tool function
        ]
