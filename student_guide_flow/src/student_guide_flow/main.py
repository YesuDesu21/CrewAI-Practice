#!/usr/bin/env python
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from student_guide_flow.crews.academics_crew.AcademicsCrew import AcademicsCrew
from student_guide_flow.crews.finance_crew.FinanceCrew import FinanceCrew
from student_guide_flow.crews.opportunity_crew.OpportunityCrew import OpportunityCrew
from student_guide_flow.crews.well_being_crew.WellBeingCrew import WellBeingCrew


class StudentGuideState(BaseModel):
    """State for the Student Guide Flow"""
    # Input data
    student_name: str = ""
    academic_data: str = ""
    financial_data: str = ""
    opportunity_preferences: str = ""
    well_being_goals: str = ""
    
    # Crew outputs
    academics_report: str = ""
    finance_report: str = ""
    opportunity_report: str = ""
    well_being_report: str = ""
    
    # Which crews to run (default: all)
    run_academics: bool = True
    run_finance: bool = True
    run_opportunity: bool = True
    run_well_being: bool = True


class StudentGuideFlow(Flow[StudentGuideState]):
    """Main flow orchestrating all student guide crews"""

    @start()
    def initialize_student_data(self, crewai_trigger_payload: dict = None):
        """Initialize student data from trigger payload or defaults"""
        print("=== Initializing Student Guide Flow ===")
        
        if crewai_trigger_payload:
            self.state.student_name = crewai_trigger_payload.get("student_name", "Student")
            self.state.academic_data = crewai_trigger_payload.get("academic_data", "")
            self.state.financial_data = crewai_trigger_payload.get("financial_data", "")
            self.state.opportunity_preferences = crewai_trigger_payload.get("opportunity_preferences", "")
            self.state.well_being_goals = crewai_trigger_payload.get("well_being_goals", "")
            
            # Optional: specify which crews to run
            self.state.run_academics = crewai_trigger_payload.get("run_academics", True)
            self.state.run_finance = crewai_trigger_payload.get("run_finance", True)
            self.state.run_opportunity = crewai_trigger_payload.get("run_opportunity", True)
            self.state.run_well_being = crewai_trigger_payload.get("run_well_being", True)
            
            print(f"Student: {self.state.student_name}")
            print(f"Running crews: Academics={self.state.run_academics}, Finance={self.state.run_finance}, "
                  f"Opportunity={self.state.run_opportunity}, Well-being={self.state.run_well_being}")
        else:
            self.state.student_name = "Student"
            print("No trigger payload provided, using defaults")

    @listen(initialize_student_data)
    def run_academics_crew(self):
        """Run the Academics crew if enabled"""
        if not self.state.run_academics:
            print("Skipping Academics crew")
            return
        
        print("\n=== Running Academics Crew ===")
        try:
            result = (
                AcademicsCrew()
                .crew()
                .kickoff(inputs={"academic_data": self.state.academic_data})
            )
            self.state.academics_report = result.raw
            print("Academics analysis completed")
        except Exception as e:
            print(f"Error in Academics crew: {e}")
            self.state.academics_report = f"Error: {str(e)}"

    @listen(initialize_student_data)
    def run_finance_crew(self):
        """Run the Finance crew if enabled"""
        if not self.state.run_finance:
            print("Skipping Finance crew")
            return
        
        print("\n=== Running Finance Crew ===")
        try:
            result = (
                FinanceCrew()
                .crew()
                .kickoff(inputs={"financial_data": self.state.financial_data})
            )
            self.state.finance_report = result.raw
            print("Finance analysis completed")
        except Exception as e:
            print(f"Error in Finance crew: {e}")
            self.state.finance_report = f"Error: {str(e)}"

    @listen(initialize_student_data)
    def run_opportunity_crew(self):
        """Run the Opportunity crew if enabled"""
        if not self.state.run_opportunity:
            print("Skipping Opportunity crew")
            return
        
        print("\n=== Running Opportunity Crew ===")
        try:
            result = (
                OpportunityCrew()
                .crew()
                .kickoff(inputs={"opportunity_preferences": self.state.opportunity_preferences})
            )
            self.state.opportunity_report = result.raw
            print("Opportunity analysis completed")
        except Exception as e:
            print(f"Error in Opportunity crew: {e}")
            self.state.opportunity_report = f"Error: {str(e)}"

    @listen(initialize_student_data)
    def run_well_being_crew(self):
        """Run the Well-being crew if enabled"""
        if not self.state.run_well_being:
            print("Skipping Well-being crew")
            return
        
        print("\n=== Running Well-being Crew ===")
        try:
            result = (
                WellBeingCrew()
                .crew()
                .kickoff(inputs={"well_being_goals": self.state.well_being_goals})
            )
            self.state.well_being_report = result.raw
            print("Well-being analysis completed")
        except Exception as e:
            print(f"Error in Well-being crew: {e}")
            self.state.well_being_report = f"Error: {str(e)}"

    @listen(run_academics_crew)
    @listen(run_finance_crew)
    @listen(run_opportunity_crew)
    @listen(run_well_being_crew)
    def compile_final_report(self):
        """Compile all crew reports into a comprehensive student guide"""
        print("\n=== Compiling Final Student Guide ===")
        
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # Create comprehensive report
        report = f"""# Student Guide Report
**Student:** {self.state.student_name}
**Generated:** {Path.cwd().name}

---

## Academic Guidance
{self.state.academics_report if self.state.academics_report else "No academic analysis performed."}

---

## Financial Guidance
{self.state.finance_report if self.state.finance_report else "No financial analysis performed."}

---

## Opportunity Guidance
{self.state.opportunity_report if self.state.opportunity_report else "No opportunity analysis performed."}

---

## Well-being Guidance
{self.state.well_being_report if self.state.well_being_report else "No well-being analysis performed."}

---
*Report generated by Student Guide AI Agent*
"""
        
        # Save individual reports
        if self.state.academics_report:
            with open(output_dir / "academics_report.md", "w") as f:
                f.write(self.state.academics_report)
        
        if self.state.finance_report:
            with open(output_dir / "finance_report.md", "w") as f:
                f.write(self.state.finance_report)
        
        if self.state.opportunity_report:
            with open(output_dir / "opportunity_report.md", "w") as f:
                f.write(self.state.opportunity_report)
        
        if self.state.well_being_report:
            with open(output_dir / "well_being_report.md", "w") as f:
                f.write(self.state.well_being_report)
        
        # Save comprehensive report
        with open(output_dir / "student_guide_report.md", "w") as f:
            f.write(report)
        
        print(f"Reports saved to {output_dir}/")
        print("Student Guide Flow completed successfully!")


def kickoff():
    """Run the student guide flow with default settings"""
    student_guide_flow = StudentGuideFlow()
    student_guide_flow.kickoff()


def plot():
    """Generate a flow visualization"""
    student_guide_flow = StudentGuideFlow()
    student_guide_flow.plot()


def run_with_trigger():
    """
    Run the flow with trigger payload.
    
    Example payload:
    {
        "student_name": "John Doe",
        "academic_data": "Current GPA: 3.8, Major: Computer Science",
        "financial_data": "Monthly income: $500, Expenses: $400",
        "opportunity_preferences": "Interested in internships and research",
        "well_being_goals": "Want to improve sleep and exercise routine",
        "run_academics": true,
        "run_finance": true,
        "run_opportunity": true,
        "run_well_being": true
    }
    """
    import json
    import sys

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    student_guide_flow = StudentGuideFlow()

    try:
        result = student_guide_flow.kickoff({"crewai_trigger_payload": trigger_payload})
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the flow with trigger: {e}")


if __name__ == "__main__":
    kickoff()
