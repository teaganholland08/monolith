import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from treasury import monolith_treasury

# 0. SETUP ENV
load_dotenv()

# 1. AUTHENTICATION (The Key)
# You will paste your key in the terminal or .env file
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = input("Enter your Google API Key: ")

# 2. THE BRAIN (LiteLLM via CrewAI)
# Ensure GEMINI_API_KEY is set for LiteLLM
os.environ["GEMINI_API_KEY"] = os.environ.get("GOOGLE_API_KEY")

# 3. THE AGENTS (Layer 1.1 of Spec)
# Using 'gemini/gemini-2.5-flash' triggers LiteLLM's Google provider
my_llm = "gemini/gemini-2.5-flash"

researcher = Agent(
    role='Market Scout',
    goal='Find high-value, low-competition niches for affiliate income.',
    backstory='You scour the internet for software tools that pay high commissions but have few reviews.',
    verbose=True,
    llm=my_llm
)

monetizer = Agent(
    role='Revenue Architect',
    goal='Turn research into a money-making asset.',
    backstory='You are an expert copywriter. You write articles that force people to click affiliate links.',
    verbose=True,
    llm=my_llm
)

# 4. THE MISSION
task_research = Task(
    description='Find 3 AI tools with affiliate programs that are trending but have under 5,000 search results on Google.',
    agent=researcher,
    expected_output='A list of 3 tools with their affiliate commission rates.'
)

task_write = Task(
    description='Write a "Top 3 Tools" Medium article based on the research. embed placeholders like [LINK] where affiliate links go.',
    agent=monetizer,
    expected_output='A full blog post formatted in Markdown.'
)

# 5. EXECUTION
profit_crew = Crew(
    agents=[researcher, monetizer],
    tasks=[task_research, task_write],
    process=Process.sequential
)

print("\n[!] MONOLITH SYSTEM: ONLINE")
result = profit_crew.kickoff()

print("\n################################")
print("##   ASSET GENERATED BELOW    ##")
print("################################\n")
print(result)

# Simulate the first potential earning (Future State)
# monolith_treasury.deposit(0.00, "Initial Run") 
