# Upwork-Proposal-Automation

AI-powered Upwork proposal generator using LangChain & Google Gemini to automate and personalize job applications.

## Pre-requisites

1. Create a virtual environment:
    ```bash
    python3 -m venv venv
    ```

2. Activate the virtual environment:
    ```bash
    source venv/bin/activate

3. Before running the script, you need to set up the `company_profile.json` file with your company’s data. Follow the structure below and replace the placeholder data with your actual company information:

  ### Sample `company_profile.json`:

  ```json
  {
    "company_name": "Your Company Name",
    "description": "A brief description of your company.",
    "core_services": [],
    "technologies": [],
    "experience_years": 0,
    "team_size": 0,
    "portfolio_projects": [
      {
        "title": "Project 1",
        "description": "Description of your project."
      },
      {
        "title": "Project 2",
        "description": "Description of your project."
      }
    ],
    "certifications": [],
    "pricing_model": "Hourly or Fixed",
    "availability": "Full-time",
    "communication_style": "professional"
  }
  ````

### Sample command to run:

```bash
python main.py generate --html-file "Developer for AI Projects - AI Apps & Integration.html" --output my_proposal.json
```

## Notes:

* Make sure that `company_profile.json` is placed in the root directory of the project.
* Ensure the HTML file (e.g., `Developer for AI Projects - AI Apps & Integration.html`) is valid and exists in the directory.

### How it works:

The script generates a personalized proposal for a job posting based on the details provided in the HTML file and your company profile.

### Additional Information:

* The proposal will be generated in a JSON format (`my_proposal.json`) which you can further customize before submitting.

## Environment Variables

1. `GOOGLE_API_KEY`: Replace with your Google API key.
2. `LANGSMITH_TRACING`: Set to `true` or `false` to enable or disable tracing.
3. `LANGSMITH_API_KEY`: Replace with your Langsmith API key.
4. `LANGSMITH_PROJECT`: Replace with your Langsmith project name.