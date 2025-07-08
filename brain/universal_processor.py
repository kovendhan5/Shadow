"""
Universal Command Processor for Shadow AI
Transforms any natural language request into actionable computer operations
"""
import logging
import json
import re
import time
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta

import google.generativeai as genai
from config import GEMINI_API_KEY

class TaskComplexity(Enum):
    SIMPLE = "simple"        # Single action
    MODERATE = "moderate"    # 2-5 steps
    COMPLEX = "complex"      # 6+ steps or conditional logic
    WORKFLOW = "workflow"    # Multi-application, context-dependent

class TaskCategory(Enum):
    DESKTOP = "desktop"              # Basic desktop operations
    DOCUMENT = "document"            # Document creation/editing
    WEB = "web"                     # Web browsing/automation
    EMAIL = "email"                 # Email management
    FILE = "file"                   # File system operations
    COMMUNICATION = "communication" # Messaging, calls
    ENTERTAINMENT = "entertainment" # Media, games
    PRODUCTIVITY = "productivity"   # Calendar, tasks, notes
    SYSTEM = "system"               # System settings, maintenance
    AUTOMATION = "automation"       # Custom workflows
    CREATIVE = "creative"           # Art, design, content creation
    RESEARCH = "research"           # Information gathering
    SHOPPING = "shopping"           # E-commerce activities
    UNIVERSAL = "universal"         # Any general request

@dataclass
class TaskStep:
    """Represents a single step in a multi-step task"""
    step_number: int
    action: str
    application: str
    parameters: Dict[str, Any]
    expected_result: str
    error_handling: str
    timeout_seconds: int = 30
    requires_confirmation: bool = False

@dataclass
class UniversalTask:
    """Represents a complete task that Shadow AI can execute"""
    task_id: str
    original_command: str
    category: TaskCategory
    complexity: TaskComplexity
    description: str
    steps: List[TaskStep]
    estimated_duration: int  # seconds
    risk_level: str  # low, medium, high
    requires_user_confirmation: bool
    context_requirements: List[str]
    success_criteria: str
    rollback_plan: Optional[str] = None

class UniversalProcessor:
    """
    Universal Command Processor that can understand and execute ANY computer task
    """
    
    def __init__(self):
        self.setup_ai()
        self.task_history = []
        self.context_memory = {}
        self.user_preferences = {}
        self.active_applications = set()
        
    def setup_ai(self):
        """Initialize AI capabilities"""
        if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_key_here":
            genai.configure(api_key=GEMINI_API_KEY)
            self.ai_model = genai.GenerativeModel('gemini-1.5-flash')
            self.ai_available = True
            logging.info("Universal Processor AI enabled")
        else:
            self.ai_available = False
            logging.warning("AI not available - using pattern-based processing")

    def process_universal_command(self, command: str, context: Dict[str, Any] = None) -> UniversalTask:
        """
        Process any natural language command into an executable task
        
        Args:
            command: Natural language command from user
            context: Optional context (current screen, active apps, etc.)
            
        Returns:
            UniversalTask: Complete task definition ready for execution
        """
        logging.info(f"Processing universal command: {command}")
        
        # Analyze command complexity and intent
        task_analysis = self._analyze_command(command, context)
        
        # Generate detailed execution plan
        if self.ai_available:
            task = self._ai_generate_task(command, task_analysis, context)
        else:
            task = self._pattern_generate_task(command, task_analysis)
            
        # Validate and optimize task
        task = self._validate_task(task)
        
        # Store in history
        self.task_history.append(task)
        
        return task

    def _analyze_command(self, command: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze command to understand intent, complexity, and requirements"""
        
        # Extract key information
        analysis = {
            "intent_keywords": self._extract_intent_keywords(command),
            "applications_mentioned": self._extract_applications(command),
            "data_entities": self._extract_data_entities(command),
            "action_verbs": self._extract_action_verbs(command),
            "time_references": self._extract_time_references(command),
            "file_references": self._extract_file_references(command),
            "web_references": self._extract_web_references(command),
            "complexity_indicators": self._assess_complexity(command),
            "risk_indicators": self._assess_risk(command),
            "context_needs": self._identify_context_needs(command, context)
        }
        
        return analysis

    def _ai_generate_task(self, command: str, analysis: Dict[str, Any], context: Dict[str, Any] = None) -> UniversalTask:
        """Use AI to generate a comprehensive task plan"""
        
        prompt = f"""
You are Shadow AI, a universal computer assistant. Break down this user request into a detailed, executable task plan.

USER COMMAND: "{command}"

ANALYSIS: {json.dumps(analysis, indent=2)}

CONTEXT: {json.dumps(context or {}, indent=2)}

Generate a comprehensive task plan with these components:

1. TASK OVERVIEW:
   - Category (desktop/document/web/email/file/communication/entertainment/productivity/system/automation/creative/research/shopping/universal)
   - Complexity (simple/moderate/complex/workflow)
   - Description
   - Estimated duration
   - Risk level (low/medium/high)

2. EXECUTION STEPS:
   For each step, provide:
   - Step number and action description
   - Application to use
   - Specific parameters/inputs
   - Expected result
   - Error handling approach
   - Timeout duration

3. REQUIREMENTS:
   - Context requirements
   - User confirmation needs
   - Success criteria
   - Rollback plan if needed

Format your response as a valid JSON object matching this structure:
{{
    "category": "category_name",
    "complexity": "complexity_level",
    "description": "Clear description of what will be done",
    "estimated_duration": duration_in_seconds,
    "risk_level": "low/medium/high",
    "requires_user_confirmation": boolean,
    "steps": [
        {{
            "step_number": 1,
            "action": "action_description",
            "application": "application_name",
            "parameters": {{"key": "value"}},
            "expected_result": "what_should_happen",
            "error_handling": "how_to_handle_errors",
            "timeout_seconds": 30,
            "requires_confirmation": false
        }}
    ],
    "context_requirements": ["requirement1", "requirement2"],
    "success_criteria": "how_to_know_if_successful",
    "rollback_plan": "how_to_undo_if_needed"
}}

IMPORTANT: Always provide safe, practical steps that respect user privacy and system security.
"""

        try:
            response = self.ai_model.generate_content(prompt)
            task_data = json.loads(response.text)
            
            # Create UniversalTask object
            return UniversalTask(
                task_id=f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                original_command=command,
                category=TaskCategory(task_data.get("category", "universal")),
                complexity=TaskComplexity(task_data.get("complexity", "simple")),
                description=task_data.get("description", "AI-generated task"),
                steps=[TaskStep(**step) for step in task_data.get("steps", [])],
                estimated_duration=task_data.get("estimated_duration", 60),
                risk_level=task_data.get("risk_level", "low"),
                requires_user_confirmation=task_data.get("requires_user_confirmation", False),
                context_requirements=task_data.get("context_requirements", []),
                success_criteria=task_data.get("success_criteria", "Task completed"),
                rollback_plan=task_data.get("rollback_plan")
            )
            
        except Exception as e:
            logging.error(f"AI task generation failed: {e}")
            return self._pattern_generate_task(command, analysis)

    def _pattern_generate_task(self, command: str, analysis: Dict[str, Any]) -> UniversalTask:
        """Fallback pattern-based task generation"""
        
        command_lower = command.lower()
        
        # Document creation patterns
        if any(phrase in command_lower for phrase in ["write", "create document", "draft", "compose"]):
            if "article" in command_lower:
                return self._create_article_task(command, analysis)
            elif "letter" in command_lower:
                return self._create_letter_task(command, analysis)
            elif "report" in command_lower:
                return self._create_report_task(command, analysis)
            else:
                return self._create_generic_document_task(command, analysis)
        
        # Web automation patterns
        elif any(phrase in command_lower for phrase in ["search", "buy", "shop", "website", "browse"]):
            return self._create_web_task(command, analysis)
        
        # File operations
        elif any(phrase in command_lower for phrase in ["file", "folder", "save", "open", "copy", "move"]):
            return self._create_file_task(command, analysis)
        
        # Email patterns
        elif any(phrase in command_lower for phrase in ["email", "mail", "send message"]):
            return self._create_email_task(command, analysis)
        
        # System operations
        elif any(phrase in command_lower for phrase in ["screenshot", "settings", "volume", "brightness"]):
            return self._create_system_task(command, analysis)
        
        # Default fallback
        else:
            return self._create_default_task(command, analysis)

    def _create_article_task(self, command: str, analysis: Dict[str, Any]) -> UniversalTask:
        """Create task for article writing with file saving"""
        
        # Extract topic
        topic = "AI"  # Default to AI topic
        if "about" in command.lower():
            topic_match = re.search(r"about\s+(.+?)(?:\s+in|\s+for|\s+on|$)", command.lower())
            if topic_match:
                topic = topic_match.group(1).strip()
        
        # Extract filename
        filename = "new.txt"  # Default filename
        if "name it" in command.lower() or "save as" in command.lower():
            filename_match = re.search(r"(?:name it|save as)\s+([^\s]+(?:\.[a-zA-Z]+)?)", command.lower())
            if filename_match:
                filename = filename_match.group(1).strip()
        
        # Check if it's the complex notepad task (open + create + name + write)
        is_complex_task = all(keyword in command.lower() for keyword in ["open", "notepad", "create", "file", "write"])
        
        if is_complex_task:
            # Use the comprehensive notepad handler
            steps = [
                TaskStep(
                    step_number=1,
                    action="open_notepad_create_file_write_article",
                    application="notepad",
                    parameters={"topic": topic, "filename": filename},
                    expected_result=f"Notepad opened, article written, and saved as {filename}",
                    error_handling="Retry with simplified approach if fails",
                    timeout_seconds=60
                )
            ]
            
            return UniversalTask(
                task_id=f"notepad_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                original_command=command,
                category=TaskCategory.DOCUMENT,
                complexity=TaskComplexity.COMPLEX,
                description=f"Open Notepad, create and save {filename} with {topic} article",
                steps=steps,
                estimated_duration=30,
                risk_level="low",
                requires_user_confirmation=False,
                context_requirements=["notepad_available"],
                success_criteria=f"File {filename} created with article content"
            )
        else:
            # Standard article creation
            steps = [
                TaskStep(
                    step_number=1,
                    action="open_notepad",
                    application="notepad",
                    parameters={},
                    expected_result="Notepad opens successfully",
                    error_handling="Try alternative text editor if Notepad fails"
                ),
                TaskStep(
                    step_number=2,
                    action="generate_article_content",
                    application="ai_generator",
                    parameters={"topic": topic, "length": "medium"},
                    expected_result="Article content generated",
                    error_handling="Use template if AI generation fails"
                ),
                TaskStep(
                    step_number=3,
                    action="type_content",
                    application="notepad",
                    parameters={"text": "{{generated_content}}"},
                    expected_result="Content typed into Notepad",
                    error_handling="Retry typing if interrupted"
                )
            ]
            
            return UniversalTask(
                task_id=f"article_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                original_command=command,
                category=TaskCategory.DOCUMENT,
                complexity=TaskComplexity.MODERATE,
                description=f"Create an article about {topic}",
                steps=steps,
                estimated_duration=120,
                risk_level="low",
                requires_user_confirmation=False,
                context_requirements=["text_editor_available"],
                success_criteria="Article content displayed in text editor"
            )

    def _extract_intent_keywords(self, command: str) -> List[str]:
        """Extract keywords that indicate user intent"""
        intent_patterns = {
            "create": ["create", "make", "build", "generate", "write", "compose", "draft"],
            "open": ["open", "launch", "start", "run", "execute"],
            "search": ["search", "find", "look for", "locate", "discover"],
            "edit": ["edit", "modify", "change", "update", "revise"],
            "send": ["send", "share", "transmit", "email", "message"],
            "save": ["save", "store", "keep", "preserve", "backup"],
            "delete": ["delete", "remove", "erase", "clear", "destroy"],
            "copy": ["copy", "duplicate", "clone", "replicate"],
            "move": ["move", "transfer", "relocate", "shift"],
            "browse": ["browse", "surf", "navigate", "visit"],
            "download": ["download", "get", "fetch", "retrieve"],
            "upload": ["upload", "post", "publish", "submit"],
            "schedule": ["schedule", "plan", "arrange", "book"],
            "analyze": ["analyze", "examine", "study", "review"],
            "automate": ["automate", "script", "batch", "routine"]
        }
        
        found_intents = []
        command_lower = command.lower()
        
        for intent, keywords in intent_patterns.items():
            if any(keyword in command_lower for keyword in keywords):
                found_intents.append(intent)
        
        return found_intents

    def _extract_applications(self, command: str) -> List[str]:
        """Extract application names mentioned in command"""
        apps = {
            "notepad": ["notepad", "text editor"],
            "word": ["word", "microsoft word", "ms word"],
            "excel": ["excel", "spreadsheet", "microsoft excel"],
            "powerpoint": ["powerpoint", "presentation", "ppt"],
            "browser": ["browser", "chrome", "firefox", "edge", "internet"],
            "calculator": ["calculator", "calc"],
            "paint": ["paint", "drawing"],
            "file_explorer": ["file explorer", "explorer", "files"],
            "outlook": ["outlook", "email client"],
            "teams": ["teams", "microsoft teams"],
            "discord": ["discord"],
            "zoom": ["zoom"],
            "spotify": ["spotify", "music"],
            "youtube": ["youtube"],
            "photoshop": ["photoshop", "ps"],
            "visual_studio": ["visual studio", "vs code", "vscode"]
        }
        
        found_apps = []
        command_lower = command.lower()
        
        for app, keywords in apps.items():
            if any(keyword in command_lower for keyword in keywords):
                found_apps.append(app)
        
        return found_apps

    def _extract_data_entities(self, command: str) -> Dict[str, List[str]]:
        """Extract data entities like names, dates, numbers, etc."""
        entities = {
            "dates": [],
            "times": [],
            "names": [],
            "numbers": [],
            "urls": [],
            "emails": [],
            "files": [],
            "locations": []
        }
        
        # Date patterns
        date_patterns = [
            r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
            r"\b(?:today|tomorrow|yesterday)\b",
            r"\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
            r"\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}\b"
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, command, re.IGNORECASE)
            entities["dates"].extend(matches)
        
        # URL patterns
        url_pattern = r"https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?|www\.(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)"
        entities["urls"] = re.findall(url_pattern, command, re.IGNORECASE)
        
        # Email patterns
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        entities["emails"] = re.findall(email_pattern, command)
        
        # File patterns
        file_pattern = r"\b\w+\.\w{2,4}\b"
        entities["files"] = re.findall(file_pattern, command)
        
        return entities

    def _extract_action_verbs(self, command: str) -> List[str]:
        """Extract action verbs from command"""
        action_verbs = [
            "create", "make", "build", "generate", "write", "compose", "draft",
            "open", "launch", "start", "run", "execute", "begin",
            "search", "find", "look", "locate", "discover", "browse",
            "edit", "modify", "change", "update", "revise", "adjust",
            "send", "share", "transmit", "email", "message", "post",
            "save", "store", "keep", "preserve", "backup", "export",
            "delete", "remove", "erase", "clear", "destroy", "cancel",
            "copy", "duplicate", "clone", "replicate", "backup",
            "move", "transfer", "relocate", "shift", "migrate",
            "download", "get", "fetch", "retrieve", "pull",
            "upload", "post", "publish", "submit", "push",
            "click", "press", "tap", "select", "choose",
            "type", "enter", "input", "write", "fill",
            "scroll", "navigate", "goto", "visit", "access",
            "close", "exit", "quit", "stop", "end",
            "minimize", "maximize", "resize", "arrange"
        ]
        
        found_verbs = []
        command_words = command.lower().split()
        
        for word in command_words:
            if word in action_verbs:
                found_verbs.append(word)
        
        return found_verbs

    def _extract_time_references(self, command: str) -> List[str]:
        """Extract time references from command"""
        time_patterns = [
            r"\b(?:now|immediately|asap|right away)\b",
            r"\b(?:in \d+\s*(?:minutes?|hours?|days?))\b",
            r"\b(?:at \d{1,2}:?\d{0,2}\s*(?:am|pm)?)\b",
            r"\b(?:today|tomorrow|yesterday)\b",
            r"\b(?:this|next|last)\s+(?:week|month|year)\b",
            r"\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b"
        ]
        
        time_refs = []
        for pattern in time_patterns:
            matches = re.findall(pattern, command, re.IGNORECASE)
            time_refs.extend(matches)
        
        return time_refs

    def _extract_file_references(self, command: str) -> List[str]:
        """Extract file and path references"""
        file_patterns = [
            r"\b\w+\.\w{2,4}\b",  # file.ext
            r"C:\\[\w\\.-]+",      # Windows paths
            r"/[\w/.-]+",          # Unix paths
            r"\\\\[\w\\.-]+",      # UNC paths
        ]
        
        files = []
        for pattern in file_patterns:
            matches = re.findall(pattern, command)
            files.extend(matches)
        
        return files

    def _extract_web_references(self, command: str) -> List[str]:
        """Extract web-related references"""
        web_patterns = [
            r"https?://[^\s]+",
            r"www\.[^\s]+",
            r"\b\w+\.com\b",
            r"\b\w+\.org\b",
            r"\b\w+\.net\b"
        ]
        
        web_refs = []
        for pattern in web_patterns:
            matches = re.findall(pattern, command, re.IGNORECASE)
            web_refs.extend(matches)
        
        return web_refs

    def _assess_complexity(self, command: str) -> str:
        """Assess command complexity based on indicators"""
        complexity_indicators = {
            "simple": ["open", "close", "click", "type", "save"],
            "moderate": ["create", "search", "edit", "send", "copy"],
            "complex": ["automate", "schedule", "integrate", "configure"],
            "workflow": ["and then", "after that", "when", "if", "while"]
        }
        
        command_lower = command.lower()
        
        # Check for workflow indicators first
        if any(indicator in command_lower for indicator in complexity_indicators["workflow"]):
            return "workflow"
        
        # Count different complexity indicators
        complexity_scores = {}
        for level, indicators in complexity_indicators.items():
            if level != "workflow":
                score = sum(1 for indicator in indicators if indicator in command_lower)
                complexity_scores[level] = score
        
        # Determine complexity based on highest score
        max_score = max(complexity_scores.values()) if complexity_scores else 0
        if max_score == 0:
            return "simple"
        
        for level, score in complexity_scores.items():
            if score == max_score:
                return level
        
        return "simple"

    def _assess_risk(self, command: str) -> str:
        """Assess risk level of command"""
        high_risk_keywords = [
            "delete", "remove", "erase", "format", "destroy", "shutdown", "restart",
            "install", "uninstall", "registry", "system", "admin", "sudo",
            "password", "credit card", "bank", "payment", "purchase", "buy"
        ]
        
        medium_risk_keywords = [
            "send", "email", "share", "upload", "post", "publish",
            "download", "access", "login", "connect", "network"
        ]
        
        command_lower = command.lower()
        
        if any(keyword in command_lower for keyword in high_risk_keywords):
            return "high"
        elif any(keyword in command_lower for keyword in medium_risk_keywords):
            return "medium"
        else:
            return "low"

    def _identify_context_needs(self, command: str, context: Dict[str, Any] = None) -> List[str]:
        """Identify what context information is needed for the task"""
        needs = []
        command_lower = command.lower()
        
        if any(word in command_lower for word in ["screen", "window", "click", "select"]):
            needs.append("current_screen")
        
        if any(word in command_lower for word in ["file", "folder", "document"]):
            needs.append("file_system_access")
        
        if any(word in command_lower for word in ["web", "browser", "website", "search"]):
            needs.append("internet_access")
        
        if any(word in command_lower for word in ["email", "send", "message"]):
            needs.append("email_access")
        
        if any(word in command_lower for word in ["this", "current", "active"]):
            needs.append("current_application")
        
        return needs

    def _validate_task(self, task: UniversalTask) -> UniversalTask:
        """Validate and optimize the generated task"""
        
        # Ensure all steps have required fields
        for i, step in enumerate(task.steps):
            if not step.action:
                step.action = f"unknown_action_{i}"
            if not step.application:
                step.application = "system"
            if not step.expected_result:
                step.expected_result = "Step completed"
            if not step.error_handling:
                step.error_handling = "Log error and continue"
        
        # Adjust risk level based on actions
        high_risk_actions = ["delete", "remove", "purchase", "send_email", "install"]
        if any(any(risk_action in step.action.lower() for risk_action in high_risk_actions) for step in task.steps):
            task.risk_level = "high"
            task.requires_user_confirmation = True
        
        # Estimate duration based on complexity and step count
        base_duration = {
            TaskComplexity.SIMPLE: 30,
            TaskComplexity.MODERATE: 120,
            TaskComplexity.COMPLEX: 300,
            TaskComplexity.WORKFLOW: 600
        }
        
        task.estimated_duration = base_duration.get(task.complexity, 60) + (len(task.steps) * 15)
        
        return task

    # Helper methods for specific task types
    def _create_letter_task(self, command: str, analysis: Dict[str, Any]) -> UniversalTask:
        """Create task for letter writing"""
        return self._create_generic_document_task(command, analysis, document_type="letter")

    def _create_report_task(self, command: str, analysis: Dict[str, Any]) -> UniversalTask:
        """Create task for report writing"""
        return self._create_generic_document_task(command, analysis, document_type="report")

    def _create_generic_document_task(self, command: str, analysis: Dict[str, Any], document_type: str = "document") -> UniversalTask:
        """Create generic document task"""
        steps = [
            TaskStep(
                step_number=1,
                action="open_text_editor",
                application="notepad",
                parameters={},
                expected_result="Text editor opens",
                error_handling="Try alternative editor"
            ),
            TaskStep(
                step_number=2,
                action="create_content",
                application="content_generator",
                parameters={"type": document_type, "command": command},
                expected_result="Content generated",
                error_handling="Use template content"
            )
        ]
        
        return UniversalTask(
            task_id=f"{document_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            original_command=command,
            category=TaskCategory.DOCUMENT,
            complexity=TaskComplexity.SIMPLE,
            description=f"Create a {document_type}",
            steps=steps,
            estimated_duration=90,
            risk_level="low",
            requires_user_confirmation=False,
            context_requirements=["text_editor_available"],
            success_criteria=f"{document_type.title()} created and displayed"
        )

    def _create_web_task(self, command: str, analysis: Dict[str, Any]) -> UniversalTask:
        """Create web automation task"""
        steps = [
            TaskStep(
                step_number=1,
                action="open_browser",
                application="browser",
                parameters={},
                expected_result="Browser opens",
                error_handling="Try alternative browser"
            )
        ]
        
        return UniversalTask(
            task_id=f"web_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            original_command=command,
            category=TaskCategory.WEB,
            complexity=TaskComplexity.MODERATE,
            description="Perform web automation",
            steps=steps,
            estimated_duration=120,
            risk_level="medium",
            requires_user_confirmation=True,
            context_requirements=["internet_access"],
            success_criteria="Web task completed"
        )

    def _create_file_task(self, command: str, analysis: Dict[str, Any]) -> UniversalTask:
        """Create file operation task"""
        return self._create_default_task(command, analysis)

    def _create_email_task(self, command: str, analysis: Dict[str, Any]) -> UniversalTask:
        """Create email task"""
        return self._create_default_task(command, analysis)

    def _create_system_task(self, command: str, analysis: Dict[str, Any]) -> UniversalTask:
        """Create system operation task"""
        if "screenshot" in command.lower():
            steps = [
                TaskStep(
                    step_number=1,
                    action="take_screenshot",
                    application="system",
                    parameters={},
                    expected_result="Screenshot saved",
                    error_handling="Retry screenshot"
                )
            ]
            
            return UniversalTask(
                task_id=f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                original_command=command,
                category=TaskCategory.SYSTEM,
                complexity=TaskComplexity.SIMPLE,
                description="Take a screenshot",
                steps=steps,
                estimated_duration=10,
                risk_level="low",
                requires_user_confirmation=False,
                context_requirements=[],
                success_criteria="Screenshot captured and saved"
            )
        
        return self._create_default_task(command, analysis)

    def _create_default_task(self, command: str, analysis: Dict[str, Any]) -> UniversalTask:
        """Create default task for unrecognized commands"""
        steps = [
            TaskStep(
                step_number=1,
                action="analyze_command",
                application="system",
                parameters={"command": command},
                expected_result="Command analyzed",
                error_handling="Report unrecognized command"
            )
        ]
        
        return UniversalTask(
            task_id=f"default_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            original_command=command,
            category=TaskCategory.UNIVERSAL,
            complexity=TaskComplexity.SIMPLE,
            description="Analyze and process command",
            steps=steps,
            estimated_duration=30,
            risk_level="low",
            requires_user_confirmation=False,
            context_requirements=[],
            success_criteria="Command processed"
        )

# Global instance
universal_processor = UniversalProcessor()

def process_universal_command(command: str, context: Dict[str, Any] = None) -> UniversalTask:
    """Main entry point for universal command processing"""
    return universal_processor.process_universal_command(command, context)
