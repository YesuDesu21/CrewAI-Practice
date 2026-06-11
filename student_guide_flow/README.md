# Student AI Guide System (Multi-Agent Flow)

An automated, localized multi-agent ecosystem designed to assist undergraduate university students in optimizing their academic journeys, managing their personal finances, tracking overall well-being, and identifying career development opportunities. 

Built on top of the **crewAI Flows** framework, the system utilizes an event-driven orchestrator to parse user intent and dynamically route tasks to four specialized, sub-nested Crews powered entirely by a local instance of **Llama 3.1**.

---

##  Architecture & Project Structure

The project consolidates multiple independent agent crews under a single parent Flow wrapper. This keeps configuration layers separate while leveraging a centralized virtual environment and unified memory/knowledge pools.

```text
student_guide_flow/
├── .env                         # Local environment configurations & dummy validations
├── pyproject.toml               # Unified project dependencies managed via uv
├── src/
│   └── student_guide_flow/
│       ├── main.py              # THE MASTER FLOW (The central routing engine)
│       │
│       ├── knowledge/           # Global RAG Memory Shared by All Crews
│       │   └── user_preference.txt  
│       │
│       ├── tools/               # Centralized Custom Tools Directory
│       │   └── __init__.py
│       │
│       └── crews/               # Specialized Sub-Crews
│           ├── academics_crew/  # Grades, workload optimization & time-blocking
│           ├── finance_crew/    # Budget audits & localized savings optimization
│           ├── opportunity_crew/# Internship scouting & campus engagement roadmaps
│           └── well_being_crew/ # Fitness/running progressions & mindfulness check-ins

##The Four Specialized Crews
The system segments distinct student life issues into dedicated operational teams:

1. Opportunity Crew
Target Areas: Internships, Scholarships, Extracurricular Organizations, Campus Events.

Agents: * Senior Career & Internship Scout: Matches a student's technical stack with upcoming professional tracks.

Campus Leadership & Engagement Strategist: Formulates custom networking and hackathon involvement blueprints.

2. Academics Crew
Target Areas: Grades Maintenance, Academic Standings, Time Management, Heavy Project Deadlines.

Agents:

Academic Performance & Curriculum Analyst: Tracks honors trajectories (e.g., Dean's List requirements) and flags course bottlenecks.

Student Time Management & Productivity Coach: Builds sustainable, high-efficiency weekly schedules.

3. Finance Crew
Target Areas: Daily Expenses, Outstanding Debts, Personal Savings Targets.

Agents:

Student Budgeting & Expense Auditor: Audits burn rates and isolates transactional budget leaks.

Strategic Savings & Debt Mitigation Advisor: Creates capital preservation game plans for milestone goals (e.g., relocation costs).

4. Overall Well Being Crew
Target Areas: Fitness Plans, Nutrition, Mental Health, Stress Tracking.

Agents:

Holistic Fitness & Endurance Coach: Tailors active strength splits and cardiovascular progressions (like 5K/10K blocks).

Empathetic Mindfulness & Mental Well-Being Advocate: Monitors emotional check-ins and provides validating, grounded psychological support.

## Local Prerequisites & Installation
This entire system runs locally on your machine, requiring no external paid API cloud keys.

1. System Dependencies
Python: >= 3.10 and < 3.14 (Python 3.13 recommended)

Ollama: Installed and running as a background service.

uv: Fast Python package installer and resolver.

2. Download the Model
Ensure your local Ollama server is hosting Llama 3.1:

PowerShell
```
ollama pull llama3.1
```

3. Standard Environment Configuration
Create an .env file in the root project directory and match this exact setup:

Code snippet
```
MODEL=ollama/llama3.1
OPENAI_API_KEY=NA
```
(Note: OPENAI_API_KEY=NA is a required dummy value used to bypass framework startup package schema validations).

4. Project Setup
Run the installation script from the project root directory to automatically build the isolated .venv using uv:

PowerShell
```
crewai install
```

## Running the Project
To execute the system, ensure you are in the primary project root directory containing the pyproject.toml file:

PowerShell
```
crewai run
```