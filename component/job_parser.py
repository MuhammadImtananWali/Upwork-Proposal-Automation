from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional

class JobDetails(BaseModel):
    title: str = Field(description="Job title")
    description: str = Field(description="Job description")
    skills_required: List[str] = Field(description="Required skills")
    budget: Optional[str] = Field(description="Budget or price range")
    timeline: Optional[str] = Field(description="Project timeline")
    company_name: Optional[str] = Field(description="Client company name")
    experience_level: Optional[str] = Field(description="Required experience level")

class JobParser:
    def __init__(self, llm):
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=JobDetails)
        
    def parse_job_content(self, content_chunks):
        prompt = PromptTemplate(
            template="""
            Extract job details from the following content:
            {content}
            
            {format_instructions}
            """,
            input_variables=["content"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        chain = prompt | self.llm | self.parser
        combined_content = " ".join(content_chunks)
        return chain.invoke({"content": combined_content})