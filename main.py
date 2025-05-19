import click
import json
from dotenv import load_dotenv

load_dotenv()

from helpers.job_extractor import JobExtractor
from helpers.job_parser import JobParser
from helpers.llm_manager import LLMManager
from helpers.profile_manager import ProfileManager
from helpers.proposal_generator import ProposalGenerator


@click.group()
def cli():
    """Upwork Proposal Automation Tool"""
    pass


@click.command()
@click.option("--html-file", help="Path to HTML file")
@click.option("--text", help="Job description text")
@click.option("--output", default="proposal.json", help="Output file")
def generate(html_file, text, output):
    """Generate a proposal from job posting"""

    # Initialize components
    llm_manager = LLMManager()
    profile_manager = ProfileManager()
    extractor = JobExtractor()
    parser = JobParser(llm_manager.llm)
    generator = ProposalGenerator(llm_manager, profile_manager)

    # Extract job details
    if html_file:
        with open(html_file, "r") as f:
            content_chunks = extractor.extract_from_html(f.read())
    elif text:
        content_chunks = extractor.process_content(text)
    else:
        click.echo("Please provide a URL, HTML file, or text")
        return

    # Parse job details
    job_details = parser.parse_job_content(content_chunks)

    # Generate proposal
    result = generator.generate_proposal(job_details)

    # Save result
    with open(output, "w") as f:
        json.dump(
            {"job_details": job_details.dict(), "proposal_result": result}, f, indent=2
        )

    click.echo(f"Proposal generated and saved to {output}")
    click.echo("\nProposal Preview:")
    click.echo(result["proposal"][:200] + "...")


@click.command()
def setup_profile():
    """Setup company profile interactively"""
    profile_manager = ProfileManager()

    click.echo("Setting up Foomotion company profile...")

    # Collect information
    description = click.prompt("Company description")
    services = click.prompt("Core services (comma-separated)").split(",")
    technologies = click.prompt("Technologies (comma-separated)").split(",")
    experience_years = click.prompt("Years of experience", type=int)
    team_size = click.prompt("Team size")

    # Update profile
    profile_manager.update_profile(
        description=description,
        core_services=[s.strip() for s in services],
        technologies=[t.strip() for t in technologies],
        experience_years=experience_years,
        team_size=team_size,
    )

    click.echo("Profile updated successfully!")


cli.add_command(generate)
cli.add_command(setup_profile)

if __name__ == "__main__":
    cli()
