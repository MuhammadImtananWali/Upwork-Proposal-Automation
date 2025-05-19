from dataclasses import dataclass
from typing import List, Dict
import json

@dataclass
class CompanyProfile:
    company_name: str = "Foomotion"
    description: str = ""
    core_services: List[str] = None
    technologies: List[str] = None
    experience_years: int = 0
    team_size: str = ""
    portfolio_projects: List[Dict] = None
    certifications: List[str] = None
    pricing_model: str = ""
    availability: str = ""
    communication_style: str = "professional"
    
    def __post_init__(self):
        if self.core_services is None:
            self.core_services = []
        if self.technologies is None:
            self.technologies = []
        if self.portfolio_projects is None:
            self.portfolio_projects = []
        if self.certifications is None:
            self.certifications = []

class ProfileManager:
    def __init__(self, profile_path="company_profile.json"):
        self.profile_path = profile_path
        self.profile = self.load_profile()
    
    def load_profile(self):
        try:
            with open(self.profile_path, 'r') as f:
                data = json.load(f)
                return CompanyProfile(**data)
        except FileNotFoundError:
            return CompanyProfile()
    
    def save_profile(self):
        with open(self.profile_path, 'w') as f:
            json.dump(self.profile.__dict__, f, indent=2)
    
    def update_profile(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self.profile, key):
                setattr(self.profile, key, value)
        self.save_profile()