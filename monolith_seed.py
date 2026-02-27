import os
from crewai import Agent, Task, Crew

# COMMANDER: Input your API Key here
# os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"

# AGENT 1: THE SCOUT
# Purpose: Finds high-value/low-competition keywords for the Monolith Manifest.
scout = Agent(
  role='Market Analyst',
  goal='Identify 3 high-ticket affiliate niches with low competition',
  backstory='Expert in SEO and digital arbitrage, focused on sovereign survival tech.',
  verbose=True
)

# AGENT 2: THE ARCHITECT
# Purpose: Writes high-converting authority articles for the niche.
architect = Agent(
  role='Content Strategist',
  goal='Draft a 1,500-word authority guide for the chosen niche',
  backstory='Specialist in technical writing and persuasive psychology.',
  verbose=True
)

# THE MISSION
task1 = Task(description='Find 3 niches for "Off-Grid Power" or "Dental Sovereignty".', agent=scout)
task2 = Task(description='Write an authority guide with placeholders for affiliate links.', agent=architect)

monolith_crew = Crew(agents=[scout, architect], tasks=[task1, task2])

if __name__ == "__main__":
    print("########## MONOLITH SEED INITIALIZED ##########")
    try:
        result = monolith_crew.kickoff()
        print("########## MISSION COMPLETE ##########")
        print(result)
    except Exception as e:
        print(f"ERROR: {e}")
        print("Ensure GOOGLE_API_KEY is set.")
