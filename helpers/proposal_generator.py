class ProposalPrompts:
    @staticmethod
    def create_proposal_prompt(job_details, company_profile, matching_data):
        # Format relevant projects for the prompt
        relevant_projects_text = ""
        if matching_data.get('relevant_projects'):
            relevant_projects_text = "\n\nRELEVANT PROJECTS TO MENTION:"
            for i, project in enumerate(matching_data.get('relevant_projects', [])[:3], 1):
                relevant_projects_text += f"\n{i}. {project.get('title')}: {project.get('description', 'Project details available upon request')}"
        
        # Format portfolio projects as backup
        portfolio_backup = ""
        if company_profile.portfolio_projects:
            portfolio_backup = "\n\nADDITIONAL PORTFOLIO PROJECTS (use if relevant projects above aren't sufficient):"
            for project in company_profile.portfolio_projects[:5]:
                if project not in matching_data.get('relevant_projects', []):
                    portfolio_backup += f"\n- {project.get('title')}: {project.get('description', 'Successful project completion')}"

        return f"""
        You are a professional freelance proposal writer. Create a compelling Upwork proposal based on the following information:

        JOB DETAILS:
        - Title: {job_details.title}
        - Description: {job_details.description}
        - Required Skills: {', '.join(job_details.skills_required)}
        - Budget: {job_details.budget or 'Not specified'}
        - Timeline: {job_details.timeline or 'Not specified'}
        - Client: {job_details.company_name or 'Potential Client'}

        COMPANY PROFILE:
        - Name: {company_profile.company_name}
        - Description: {company_profile.description}
        - Experience: {company_profile.experience_years} years in the industry
        - Team Size: {company_profile.team_size} skilled professionals
        - Core Services: {', '.join(company_profile.core_services)}
        - Technologies: {', '.join(company_profile.technologies)}

        MATCHING INFORMATION:
        - Relevance Score: {matching_data.get('relevance_score', 0):.2f}
        - Matching Skills: {', '.join(matching_data.get('matching_skills', []))}
        {relevant_projects_text}
        {portfolio_backup}

        CRITICAL REQUIREMENTS:
        1. Keep the proposal between 200-350 words
        2. Start with a personalized greeting addressing the client by name
        3. MUST mention at least 2-3 specific projects from the lists above with brief descriptions
        4. Highlight matching skills explicitly (TypeScript, React, Python, AI Chatbot, LangChain, etc.)
        5. Reference the company description to show understanding of cross-disciplinary collaboration
        6. Address the specific needs mentioned in the job description (FastAPI, Langchain/Langgraph, React+TypeScript)
        7. Include a clear call-to-action for next steps
        8. Use a professional but approachable tone
        9. NO placeholder text like "[mention if possible]" - always include specific examples
        10. Show enthusiasm for long-term collaboration as mentioned in the job post

        EXAMPLE PROJECT INTEGRATION:
        Instead of: "We have experience with similar projects"
        Write: "For example, we developed Ikigai, an AI platform for enterprises that uses generative AI for data forecasting, and created MineARC, a safety compliance platform with advanced inspection features."

        Generate a compelling, specific proposal that demonstrates our expertise with concrete examples:
        """

    @staticmethod
    def create_subject_line_prompt(job_details, company_profile):
        return f"""
        Create a compelling subject line for an Upwork proposal. The job is about: "{job_details.title}"
        
        Our company specializes in: {', '.join(company_profile.core_services[:3])}
        
        Requirements:
        1. Keep it under 60 characters
        2. Be specific and relevant
        3. Highlight our expertise
        4. Avoid generic phrases
        5. Create urgency or interest
        
        Generate 3 different subject line options:
        """

from langchain.prompts import PromptTemplate
from datetime import datetime

from profile_matcher import ProfileMatcher

class ProposalGenerator:
    def __init__(self, llm_manager, profile_manager):
        self.llm_manager = llm_manager
        self.profile_manager = profile_manager
        self.matcher = ProfileMatcher(profile_manager.profile)
    
    def generate_proposal(self, job_details, template_type="standard"):
        # Calculate matching data
        matching_data = {
            'relevance_score': self.matcher.calculate_relevance_score(job_details),
            'matching_skills': self.matcher.get_matching_skills(job_details),
            'relevant_projects': self.matcher.get_relevant_projects(job_details)
        }
        
        # Generate proposal content
        proposal_prompt = ProposalPrompts.create_proposal_prompt(
            job_details, 
            self.profile_manager.profile, 
            matching_data
        )
        
        proposal_content = self.llm_manager.generate_text(proposal_prompt)
        
        # Generate subject lines
        subject_prompt = ProposalPrompts.create_subject_line_prompt(
            job_details, 
            self.profile_manager.profile
        )
        
        subject_lines = self.llm_manager.generate_text(subject_prompt)
        
        return {
            'proposal': proposal_content,
            'subject_lines': subject_lines,
            'matching_data': matching_data,
            'generated_at': datetime.now().isoformat()
        }
    
    def refine_proposal(self, original_proposal, feedback):
        refine_prompt = f"""
        Improve the following proposal based on this feedback:
        
        ORIGINAL PROPOSAL:
        {original_proposal}
        
        FEEDBACK:
        {feedback}
        
        Generate an improved version that addresses the feedback while maintaining professionalism:
        """
        
        return self.llm_manager.generate_text(refine_prompt)