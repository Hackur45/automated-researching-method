from crewai_tools import tool
from crewai_tools.tools import FileReadTool
import os
import subprocess
import requests
import re
import urllib.request as libreq
from bs4 import BeautifulSoup
from urllib.parse import quote
import PyPDF2
import io
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_text_splitters.character import CharacterTextSplitter
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv
from searchtools import ExaSearchToolset

load_dotenv()


class ResearcherToolSet:
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
    def load_document(self,file_path_url):
        """_summary_

        Args:
            file_path_url (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            response=requests.get(file_path_url)
            response.raise_for_status() # Raise an exception for bad status codes
            
            pdf_file_obj=io.BytesIO(response.content)
            
            pdf_reader=PyPDF2.PdfReader(pdf_file_obj)
            
            text=""
            
            num_pages=min(2,len(pdf_reader.pages))
            
            for page_num in range(num_pages):
                text+=pdf_reader.pages[page_num].extract_text()

            return text
        except requests.RequestException as e:
            print(f"Error occured:{e}")
            return None
        except Exception as e:
            print(f"Error occured in processing of pdf:{e}")
            return None 
    
        
    @tool
    def load_document_to_vector_db(self, vector_db: FAISS, research_paper_path):
        """_summary_

        Args:
            vector_db (FAISS): _description_
            research_paper_path (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            # Create loader
            loader = PyPDFLoader(research_paper_path)
            
            # Load documents
            documents = loader.load()
            
            # Create embeddings
            embeddings = HuggingFaceBgeEmbeddings()
            
            # Create text splitter
            text_splitter = CharacterTextSplitter(
                separator='\n',
                chunk_size=500,
                chunk_overlap=200
            )
            
            # Split documents
            doc_chunks = text_splitter.split_documents(documents)
            
            # Add to vector db
            vector_db.add_documents(doc_chunks, embeddings)
            
            return documents
            
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
    
    
    @tool
    def web_search_tools(self):
        """_summary_

        Args:
            query (_type_): _description_
        """
        return ExaSearchToolset.tools()
    
     # for latex writer
    
    @tool
    def latex_writer_tool( resarch_latex_code, file_name: str):
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
        file_name = file_name.lower().replace(" ", "_") + ".tex"

        try:
            with open(file_name, "w") as file:
                file.write(resarch_latex_code)
        except Exception as e:
            return f"Error while creating the file: {str(e)}"


    # for latex  to pdf
    @tool
    def convert_latex_to_pdf(self, latex_file_name,output_directory="Your Resarchers"):
        """returns a pdf file with latex written

        Args:
            latex_file_name (_type_): _description_
        """
        if not os.path.exists(latex_file_name):
            print(f"Error: File '{latex_file_name}' not found .")
            return None
        
        
        try:
            pdflatex_path= subprocess.check_output(['where','pdflatex'],
                                                   stderr=subprocess.STDOUT,
                                                   text=True
                                                   )
            print(f"Found pdflatex at: {pdflatex_path}")
        except subprocess.CalledProcessError:
            print("Error : Could not find pdflatex in PATH")
            print("\nCurrent PATH environment:")
            print(os.environ.get('PATH','').replace(';','\n'))
            return None
        #non stop mode stops from any manual input given between the compilation 
        if  output_directory:
            os.makedirs(output_directory,exist_ok=True)
            command=[
                'pdflatex',
                '-interaction=nonstopmode',
                '-output-directory',
                output_directory,
                latex_file_name
            ]
        else:
            command=[
                'pdflatex',
                '-interaction=nonstopmode',
                latex_file_name
            ]
        
        try:
            print(f"Attempting to run command: {' '.join(command)}")
             
            result= subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False)
            
            if result.stderr:
                print("\nError Output :")
                print(result.stderr)
                
            
            if result.returncode==0:
                print("PDF compiled successfully!")
                pdf_file=os.path.splitext(os.path.basename(latex_file_name))[0]+".pdf"
                return os.path.join(output_directory or ".",pdf_file)
            else:
                print("Compilation failed")
                print(result.stderr)
        except FileNotFoundError:
            print( "File not found")
            return NotImplemented

    def latex_conver_tools(): 
        return[
            ResearcherToolSet.convert_latex_to_pdf,
            ResearcherToolSet.latex_writer_tool
        ]   
    
    def resarch_tools():
        return[
            ResearcherToolSet.arxiv_research_tool,
            ResearcherToolSet.web_search_tools,
            ResearcherToolSet.load_document,
        ]
        
    """ def storage_tools():
        return[
            ResearcherToolSet.load_document_to_vector_db
        ] """