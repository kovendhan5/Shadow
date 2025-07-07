# examples/automation_workflows.py
"""
Advanced automation workflows for Shadow AI Agent
This script demonstrates complex multi-step automation tasks
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import ShadowAI
from task_manager import task_manager, create_task_from_template
import time

def job_application_workflow():
    """Demonstrate job application workflow"""
    print("💼 Job Application Workflow")
    print("=" * 40)
    
    shadow = ShadowAI()
    
    steps = [
        "create a resume template",
        "open browser",
        "search for jobs on naukri.com",
        "take a screenshot of job listings"
    ]
    
    print("This workflow will help you with job applications:")
    for i, step in enumerate(steps, 1):
        print(f"{i}. {step}")
    
    print("\nExecuting workflow...")
    
    for step in steps:
        print(f"\n🔄 Step: {step}")
        shadow.run_single_command(step)
        time.sleep(2)
    
    print("\n✅ Job application workflow completed!")

def document_workflow():
    """Demonstrate document creation workflow"""
    print("\n📄 Document Creation Workflow")
    print("=" * 40)
    
    shadow = ShadowAI()
    
    # Create multiple documents
    documents = [
        ("leave letter", "write a leave letter for next Friday due to family function"),
        ("meeting notes", "create a document for meeting notes"),
        ("project proposal", "create a document for project proposal")
    ]
    
    print("Creating multiple documents:")
    for doc_name, command in documents:
        print(f"\n📝 Creating {doc_name}...")
        shadow.run_single_command(command)
        time.sleep(2)
    
    print("\n✅ Document workflow completed!")

def research_workflow():
    """Demonstrate research workflow"""
    print("\n🔍 Research Workflow")
    print("=" * 40)
    
    shadow = ShadowAI()
    
    research_topics = [
        "artificial intelligence trends",
        "machine learning applications",
        "automation in business"
    ]
    
    print("Researching multiple topics:")
    for topic in research_topics:
        print(f"\n🔍 Researching: {topic}")
        shadow.run_single_command(f"search for {topic} on google")
        time.sleep(3)
        
        # Take screenshot of results
        shadow.run_single_command(f"take a screenshot")
        time.sleep(1)
    
    print("\n✅ Research workflow completed!")

def productivity_workflow():
    """Demonstrate productivity workflow"""
    print("\n⚡ Productivity Workflow")
    print("=" * 40)
    
    shadow = ShadowAI()
    
    # Morning productivity routine
    tasks = [
        ("open calculator", "Opening calculator for quick calculations"),
        ("open notepad", "Opening notepad for notes"),
        ("take a screenshot", "Taking screenshot of current desktop"),
        ("open explorer", "Opening file explorer")
    ]
    
    print("Morning productivity setup:")
    for command, description in tasks:
        print(f"\n⚡ {description}")
        shadow.run_single_command(command)
        time.sleep(2)
    
    print("\n✅ Productivity workflow completed!")

def e_commerce_workflow():
    """Demonstrate e-commerce workflow"""
    print("\n🛒 E-commerce Workflow")
    print("=" * 40)
    
    shadow = ShadowAI()
    
    # Shopping workflow
    products = [
        "smartphone",
        "laptop",
        "headphones"
    ]
    
    print("Shopping research workflow:")
    for product in products:
        print(f"\n🛒 Searching for {product}...")
        shadow.run_single_command(f"search for {product} on flipkart")
        time.sleep(3)
        
        # Take screenshot for comparison
        shadow.run_single_command("take a screenshot")
        time.sleep(1)
    
    print("\n✅ E-commerce workflow completed!")

def advanced_task_workflow():
    """Demonstrate advanced task management"""
    print("\n🚀 Advanced Task Management")
    print("=" * 40)
    
    # Create complex tasks using task manager
    task1 = create_task_from_template("leave_letter", {"reason": "health reasons"})
    task2 = create_task_from_template("product_search", {"product": "iPhone", "site": "flipkart"})
    
    if task1:
        print(f"📋 Created task: {task1.name}")
        task_manager.execute_task(task1.id)
    
    if task2:
        print(f"📋 Created task: {task2.name}")
        task_manager.execute_task(task2.id)
    
    # Show task progress
    tasks = task_manager.list_tasks()
    print("\n📊 Task Status:")
    for task in tasks:
        print(f"• {task['name']}: {task['status']}")
    
    print("\n✅ Advanced task workflow completed!")

def custom_workflow():
    """Create a custom workflow based on user input"""
    print("\n🎯 Custom Workflow Creator")
    print("=" * 40)
    
    shadow = ShadowAI()
    
    print("Let's create a custom workflow for you!")
    print("Enter commands one by one (empty line to finish):")
    
    commands = []
    while True:
        command = input("Command: ").strip()
        if not command:
            break
        commands.append(command)
    
    if commands:
        print(f"\n🔄 Executing {len(commands)} commands...")
        for i, command in enumerate(commands, 1):
            print(f"\n{i}. {command}")
            shadow.run_single_command(command)
            time.sleep(2)
        
        print("\n✅ Custom workflow completed!")
    else:
        print("No commands entered.")

def main():
    """Main function"""
    print("🚀 Shadow AI Advanced Automation Workflows")
    print("=" * 60)
    
    print("\nAvailable workflows:")
    print("1. Job Application Workflow")
    print("2. Document Creation Workflow")
    print("3. Research Workflow")
    print("4. Productivity Workflow")
    print("5. E-commerce Workflow")
    print("6. Advanced Task Management")
    print("7. Custom Workflow")
    print("8. Run All Workflows")
    
    try:
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            job_application_workflow()
        elif choice == '2':
            document_workflow()
        elif choice == '3':
            research_workflow()
        elif choice == '4':
            productivity_workflow()
        elif choice == '5':
            e_commerce_workflow()
        elif choice == '6':
            advanced_task_workflow()
        elif choice == '7':
            custom_workflow()
        elif choice == '8':
            print("Running all workflows with 5-second delays...")
            workflows = [
                job_application_workflow,
                document_workflow,
                research_workflow,
                productivity_workflow,
                e_commerce_workflow,
                advanced_task_workflow
            ]
            
            for workflow in workflows:
                workflow()
                time.sleep(5)
        else:
            print("Invalid choice. Running job application workflow...")
            job_application_workflow()
        
        print("\n🎉 Workflow demonstration completed!")
        print("\nYou can create your own workflows by combining Shadow AI commands.")
        print("Use the task manager for complex multi-step automations.")
        
    except KeyboardInterrupt:
        print("\n\n👋 Workflows stopped by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check your Shadow AI installation and try again.")

if __name__ == "__main__":
    main()
