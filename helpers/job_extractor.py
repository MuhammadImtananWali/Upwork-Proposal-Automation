from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
import re

class JobExtractor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    def extract_from_url(self, url):
        loader = WebBaseLoader(url)
        documents = loader.load()
        return self.process_content(documents[0].page_content)
    
    def extract_from_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        return self.process_content(text)
    
    def process_content(self, content):
        # Clean and structure the content
        cleaned_content = re.sub(r'\s+', ' ', content).strip()
        return self.text_splitter.split_text(cleaned_content)