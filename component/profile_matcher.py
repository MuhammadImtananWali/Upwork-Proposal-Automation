from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ProfileMatcher:
    def __init__(self, company_profile):
        self.company_profile = company_profile
        self.vectorizer = TfidfVectorizer(stop_words='english')
    
    def calculate_relevance_score(self, job_details):
        # Combine company services and technologies
        company_text = " ".join(
            self.company_profile.core_services + 
            self.company_profile.technologies
        ).lower()
        
        # Combine job requirements
        job_text = " ".join(
            job_details.skills_required + 
            [job_details.description]
        ).lower()
        
        # Calculate similarity
        if company_text and job_text:
            vectors = self.vectorizer.fit_transform([company_text, job_text])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            return similarity
        return 0.0
    
    def get_matching_skills(self, job_details):
        company_skills = set(skill.lower() for skill in 
                           self.company_profile.core_services + 
                           self.company_profile.technologies)
        job_skills = set(skill.lower() for skill in job_details.skills_required)
        return list(company_skills.intersection(job_skills))
    
    def get_relevant_projects(self, job_details, max_projects=3):
        if not self.company_profile.portfolio_projects:
            return []
        
        # Create a combined search text from job details
        job_search_terms = [
            job_details.title.lower(),
            job_details.description.lower(),
            ' '.join(job_details.skills_required).lower()
        ]
        job_text = ' '.join(job_search_terms)
        
        # Score projects based on relevance to job
        scored_projects = []
        
        for project in self.company_profile.portfolio_projects:
            # Create searchable text for project
            project_terms = [
                project.get('title', '').lower(),
                project.get('description', '').lower()
            ]
            project_text = ' '.join(project_terms)
            
            # Calculate relevance score
            score = 0.0
            if project_text and job_text:
                try:
                    # Use TF-IDF for better matching
                    vectors = self.vectorizer.fit_transform([project_text, job_text])
                    if vectors.shape[0] > 1:
                        score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
                except:
                    # Fallback to simple keyword matching
                    job_keywords = set(job_text.split())
                    project_keywords = set(project_text.split())
                    if project_keywords:
                        score = len(job_keywords.intersection(project_keywords)) / len(project_keywords.union(job_keywords))
            
            # Boost score for projects with relevant keywords
            relevant_keywords = [
                'ai', 'artificial intelligence', 'machine learning', 'langchain',
                'fastapi', 'react', 'typescript', 'python', 'api', 'chatbot',
                'fintech', 'saas', 'platform', 'enterprise', 'web development'
            ]
            
            for keyword in relevant_keywords:
                if keyword in job_text and keyword in project_text:
                    score += 0.1  # Boost score for keyword matches
            
            scored_projects.append((project, score))
        
        # Sort by relevance score
        scored_projects.sort(key=lambda x: x[1], reverse=True)
        
        # Return top projects, ensuring we have at least some projects even if scores are low
        top_projects = [project for project, score in scored_projects[:max_projects]]
        
        # If we don't have enough projects or scores are very low, add some high-impact projects
        if len(top_projects) < max_projects or all(score < 0.1 for _, score in scored_projects[:max_projects]):
            # Add some flagship projects that showcase capabilities
            flagship_projects = [
                proj for proj in self.company_profile.portfolio_projects 
                if proj.get('title') in ['ikigai', 'Cheddar Up', 'Mrsool', 'Cambrilearn', 'KnowMy']
                and proj not in top_projects
            ]
            
            # Fill remaining slots with flagship projects
            remaining_slots = max_projects - len(top_projects)
            top_projects.extend(flagship_projects[:remaining_slots])
        
        return top_projects[:max_projects]