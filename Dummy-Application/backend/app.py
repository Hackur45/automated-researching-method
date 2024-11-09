from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API"))

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_research_paper(content):
    try:
        logger.info("Generating research paper based on the scraped content...")

        prompt = f"""
        Based on the following scraped content, generate a detailed research paper in Markdown format with the following sections:
        - # Introduction: Explain the research problem or topic.
        - ## Methodology: Describe the approach and methods used for gathering and analyzing data.
        - ## Results: Present the findings based on the content with bulleted lists and bold text for key points.
        - ## Discussion: Analyze the results and discuss implications, using bold text to highlight major insights.
        - ## Conclusion: Provide a summary of findings and implications.
        - ### Further Research: Propose additional areas of study.
        
        Ensure all headings, bullet points, and bold text are in proper Markdown format for clear formatting in CKEditor.
        
        Scraped Content:
        {content}
        """

        # Use Gemini 1.5 Flash model for text generation
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        logger.info("AI Research Paper Generated.")
        return response.text.strip() if response else "No response from Gemini API."

    except Exception as e:
        logger.error(f"Error generating research paper: {e}")
        return None

@app.route('/api/research', methods=['POST'])
def google_search_research():
    data = request.json
    query = data.get("query")

    # Initialize WebDriver options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    results = []

    try:
        logger.info(f"Searching for query: {query}")
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Wait for the results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//h3/a"))
        )

        # Get URLs and store in a list to avoid stale element issues
        urls = [link.get_attribute("href") for link in driver.find_elements(By.XPATH, "//h3/a")[:5]]

        for url in urls:
            logger.info(f"Visiting URL: {url}")
            driver.get(url)
            time.sleep(3)

            try:
                retry_attempts = 3
                paragraphs = []
                for attempt in range(retry_attempts):
                    try:
                        paragraphs = driver.find_elements(By.TAG_NAME, "p")
                        if paragraphs:
                            break
                    except StaleElementReferenceException:
                        logger.warning(f"StaleElementReferenceException occurred. Retrying {attempt+1}/{retry_attempts}...")
                        time.sleep(2)
                    except TimeoutException:
                        logger.error(f"TimeoutException: Could not retrieve content from {url} in time.")
                        break

                if paragraphs:
                    content = {
                        "url": url,
                        "paragraphs": [para.text for para in paragraphs[:5]]
                    }
                    results.append(content)
                    logger.info(f"Scraped Content from {url}: {content['paragraphs']}")
                else:
                    logger.warning(f"No paragraphs found on page: {url}")
            except Exception as e:
                logger.error(f"Could not extract content from {url}: {e}")

        if not results:
            logger.warning(f"No valid research data found for query: {query}")

        # Combine paragraphs from all fetched URLs for AI model
        combined_content = "\n".join([item['paragraphs'][0] for item in results if item['paragraphs']])
        logger.info("Combined Scraped Content for AI:")

        ai_research_paper = generate_research_paper(combined_content)

        response = {
            "research_data": results if results else [],
            "ai_research_paper": ai_research_paper if ai_research_paper else "No paper generated"
        }

        return jsonify(response)

    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=True)
