# task_manager.py
"""
Shadow AI Task Manager
Manages and executes complex multi-step tasks
"""

import logging
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from utils.confirm import confirm_action
from brain.gpt_agent import process_command

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class TaskStep:
    """Represents a single step in a task"""
    id: str
    description: str
    action: str
    parameters: Dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    confirmation_required: bool = False

@dataclass
class Task:
    """Represents a complete task with multiple steps"""
    id: str
    name: str
    description: str
    steps: List[TaskStep]
    status: TaskStatus = TaskStatus.PENDING
    created_at: float = 0
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    
    def __post_init__(self):
        if self.created_at == 0:
            self.created_at = time.time()

class TaskManager:
    """Manages and executes tasks"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.current_task: Optional[Task] = None
        self.task_counter = 0
    
    def create_task(self, name: str, description: str, command: str = None) -> Task:
        """Create a new task"""
        self.task_counter += 1
        task_id = f"task_{self.task_counter}_{int(time.time())}"
        
        if command:
            # Use AI to break down command into steps
            steps = self._generate_task_steps(command)
        else:
            steps = []
        
        task = Task(
            id=task_id,
            name=name,
            description=description,
            steps=steps
        )
        
        self.tasks[task_id] = task
        logging.info(f"Created task: {task_id} - {name}")
        return task
    
    def _generate_task_steps(self, command: str) -> List[TaskStep]:
        """Generate task steps from command using AI"""
        try:
            # Use GPT agent to break down command
            action_data = process_command(command)
            
            step = TaskStep(
                id="step_1",
                description=action_data.get('description', 'Execute command'),
                action=action_data.get('action', 'unknown'),
                parameters=action_data.get('parameters', {}),
                confirmation_required=action_data.get('confirmation_required', False)
            )
            
            return [step]
        except Exception as e:
            logging.error(f"Error generating task steps: {e}")
            return []
    
    def add_step(self, task_id: str, description: str, action: str, parameters: Dict[str, Any], 
                 confirmation_required: bool = False) -> bool:
        """Add a step to an existing task"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        step_id = f"step_{len(task.steps) + 1}"
        
        step = TaskStep(
            id=step_id,
            description=description,
            action=action,
            parameters=parameters,
            confirmation_required=confirmation_required
        )
        
        task.steps.append(step)
        logging.info(f"Added step to task {task_id}: {description}")
        return True
    
    def execute_task(self, task_id: str) -> bool:
        """Execute a task"""
        if task_id not in self.tasks:
            logging.error(f"Task not found: {task_id}")
            return False
        
        task = self.tasks[task_id]
        self.current_task = task
        
        logging.info(f"Starting task execution: {task.name}")
        task.status = TaskStatus.RUNNING
        task.started_at = time.time()
        
        try:
            for step in task.steps:
                if not self._execute_step(step):
                    task.status = TaskStatus.FAILED
                    logging.error(f"Task failed at step: {step.description}")
                    return False
            
            task.status = TaskStatus.COMPLETED
            task.completed_at = time.time()
            logging.info(f"Task completed successfully: {task.name}")
            return True
        
        except Exception as e:
            task.status = TaskStatus.FAILED
            logging.error(f"Task execution error: {e}")
            return False
        finally:
            self.current_task = None
    
    def _execute_step(self, step: TaskStep) -> bool:
        """Execute a single step"""
        step.status = TaskStatus.RUNNING
        logging.info(f"Executing step: {step.description}")
        
        try:
            # Check for confirmation if required
            if step.confirmation_required:
                if not confirm_action(step.description):
                    step.status = TaskStatus.CANCELLED
                    logging.info(f"Step cancelled by user: {step.description}")
                    return False
            
            # Execute the step (this would integrate with the main execution engine)
            success = self._perform_action(step.action, step.parameters)
            
            if success:
                step.status = TaskStatus.COMPLETED
                logging.info(f"Step completed: {step.description}")
                return True
            else:
                step.status = TaskStatus.FAILED
                logging.error(f"Step failed: {step.description}")
                return False
        
        except Exception as e:
            step.status = TaskStatus.FAILED
            step.error = str(e)
            logging.error(f"Step execution error: {e}")
            return False
    
    def _perform_action(self, action: str, parameters: Dict[str, Any]) -> bool:
        """Perform the actual action (placeholder - would integrate with main system)"""
        # This would integrate with the main execution system
        # For now, just simulate success
        time.sleep(0.5)  # Simulate work
        return True
    
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """Get the status of a task"""
        if task_id not in self.tasks:
            return None
        return self.tasks[task_id].status
    
    def get_task_progress(self, task_id: str) -> Dict[str, Any]:
        """Get detailed progress of a task"""
        if task_id not in self.tasks:
            return {}
        
        task = self.tasks[task_id]
        total_steps = len(task.steps)
        completed_steps = sum(1 for step in task.steps if step.status == TaskStatus.COMPLETED)
        
        return {
            'task_id': task_id,
            'name': task.name,
            'description': task.description,
            'status': task.status.value,
            'total_steps': total_steps,
            'completed_steps': completed_steps,
            'progress_percentage': (completed_steps / total_steps * 100) if total_steps > 0 else 0,
            'created_at': task.created_at,
            'started_at': task.started_at,
            'completed_at': task.completed_at,
            'steps': [
                {
                    'id': step.id,
                    'description': step.description,
                    'status': step.status.value,
                    'error': step.error
                }
                for step in task.steps
            ]
        }
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a task"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        task.status = TaskStatus.CANCELLED
        
        # Cancel any running steps
        for step in task.steps:
            if step.status == TaskStatus.RUNNING:
                step.status = TaskStatus.CANCELLED
        
        logging.info(f"Task cancelled: {task.name}")
        return True
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """List all tasks"""
        return [
            {
                'id': task.id,
                'name': task.name,
                'description': task.description,
                'status': task.status.value,
                'created_at': task.created_at,
                'step_count': len(task.steps)
            }
            for task in self.tasks.values()
        ]
    
    def cleanup_completed_tasks(self) -> int:
        """Remove completed tasks older than 24 hours"""
        current_time = time.time()
        to_remove = []
        
        for task_id, task in self.tasks.items():
            if (task.status == TaskStatus.COMPLETED and 
                task.completed_at and 
                current_time - task.completed_at > 86400):  # 24 hours
                to_remove.append(task_id)
        
        for task_id in to_remove:
            del self.tasks[task_id]
        
        logging.info(f"Cleaned up {len(to_remove)} completed tasks")
        return len(to_remove)

# Global task manager instance
task_manager = TaskManager()

# Predefined task templates
TASK_TEMPLATES = {
    "leave_letter": {
        "name": "Create Leave Letter",
        "description": "Generate and save a leave letter document",
        "steps": [
            {
                "description": "Generate leave letter content",
                "action": "generate_leave_letter",
                "parameters": {}
            },
            {
                "description": "Save as Word document",
                "action": "save_document",
                "parameters": {"format": "docx"}
            }
        ]
    },
    "product_search": {
        "name": "Search Product Online",
        "description": "Search for a product on e-commerce website",
        "steps": [
            {
                "description": "Open browser",
                "action": "open_browser",
                "parameters": {}
            },
            {
                "description": "Navigate to website",
                "action": "navigate_to_site",
                "parameters": {}
            },
            {
                "description": "Search for product",
                "action": "search_product",
                "parameters": {}
            }
        ]
    },
    "resume_upload": {
        "name": "Upload Resume",
        "description": "Upload resume to job portal",
        "steps": [
            {
                "description": "Open job portal",
                "action": "open_browser",
                "parameters": {}
            },
            {
                "description": "Navigate to upload section",
                "action": "navigate_to_upload",
                "parameters": {}
            },
            {
                "description": "Upload resume file",
                "action": "upload_file",
                "parameters": {},
                "confirmation_required": True
            }
        ]
    }
}

def create_task_from_template(template_name: str, parameters: Dict[str, Any] = None) -> Optional[Task]:
    """Create a task from a predefined template"""
    if template_name not in TASK_TEMPLATES:
        logging.error(f"Template not found: {template_name}")
        return None
    
    template = TASK_TEMPLATES[template_name]
    task = task_manager.create_task(
        name=template["name"],
        description=template["description"]
    )
    
    # Add steps from template
    for step_data in template["steps"]:
        step_params = step_data["parameters"].copy()
        if parameters:
            step_params.update(parameters)
        
        task_manager.add_step(
            task_id=task.id,
            description=step_data["description"],
            action=step_data["action"],
            parameters=step_params,
            confirmation_required=step_data.get("confirmation_required", False)
        )
    
    return task
