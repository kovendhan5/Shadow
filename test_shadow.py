# test_shadow.py
"""
Test suite for Shadow AI Agent
Run with: python -m pytest test_shadow.py -v
"""

import pytest
import os
import sys
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment variables for testing
os.environ['OPENAI_API_KEY'] = 'test_key_not_real'
os.environ['GEMINI_API_KEY'] = 'test_key_not_real'
os.environ['OLLAMA_URL'] = 'http://localhost:11434'

from config import DESKTOP_PATH, DOCUMENTS_PATH
from brain.gpt_agent import process_command, GPTAgent
from control.desktop import DesktopController
from control.documents import DocumentController
from utils.confirm import ConfirmationManager
from utils.logging import setup_logging
from task_manager import TaskManager, TaskStatus

class TestGPTAgent:
    """Test the GPT Agent functionality"""
    
    def test_fallback_command_parsing(self):
        """Test fallback command parsing"""
        # Test open notepad
        result = process_command("open notepad")
        assert result['task_type'] == 'desktop_control'
        assert result['action'] == 'open_notepad'
        
        # Test type command
        result = process_command("type: Hello World")
        assert result['task_type'] == 'desktop_control'
        assert result['action'] == 'type_text'
        assert result['parameters']['text'] == 'Hello World'
        
        # Test click command
        result = process_command("click at 100, 200")
        assert result['task_type'] == 'desktop_control'
        assert result['action'] == 'click_at'
        assert result['parameters']['x'] == 100
        assert result['parameters']['y'] == 200
    
    def test_unknown_command(self):
        """Test handling of unknown commands"""
        result = process_command("unknown command")
        assert result['task_type'] == 'unknown'
        assert result['action'] == 'unknown_command'
    
    @patch('brain.gpt_agent.GEMINI_API_KEY', 'test_key')
    def test_gpt_agent_initialization(self):
        """Test GPT Agent initialization"""
        with patch('google.generativeai.configure'):
            agent = GPTAgent(provider='gemini')
            assert agent.provider == 'gemini'
            assert agent.model == 'gemini-pro'

class TestDesktopController:
    """Test Desktop Controller functionality"""
    
    def test_desktop_controller_init(self):
        """Test desktop controller initialization"""
        controller = DesktopController()
        assert controller.screen_width > 0
        assert controller.screen_height > 0
    
    @patch('subprocess.Popen')
    def test_open_notepad(self, mock_popen):
        """Test opening notepad"""
        controller = DesktopController()
        result = controller.open_notepad()
        assert result == True
        mock_popen.assert_called_once_with(["notepad.exe"])
    
    @patch('subprocess.Popen')
    def test_open_calculator(self, mock_popen):
        """Test opening calculator"""
        controller = DesktopController()
        result = controller.open_calculator()
        assert result == True
        mock_popen.assert_called_once_with(["calc.exe"])
    
    @patch('pyautogui.typewrite')
    def test_type_text(self, mock_typewrite):
        """Test typing text"""
        controller = DesktopController()
        result = controller.type_text("Hello World")
        assert result == True
        mock_typewrite.assert_called_once_with("Hello World", interval=0.1)
    
    @patch('pyautogui.click')
    def test_click_at(self, mock_click):
        """Test clicking at coordinates"""
        controller = DesktopController()
        result = controller.click_at(100, 200)
        assert result == True
        mock_click.assert_called_once_with(100, 200, button='left', clicks=1)
    
    def test_click_out_of_bounds(self):
        """Test clicking outside screen bounds"""
        controller = DesktopController()
        result = controller.click_at(-100, -100)
        assert result == False

class TestDocumentController:
    """Test Document Controller functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.controller = DocumentController()
        self.controller.desktop_path = self.temp_dir
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_create_txt_document(self):
        """Test creating a text document"""
        self.setUp()
        try:
            result = self.controller._create_txt("Test content", 
                                                os.path.join(self.temp_dir, "test.txt"))
            assert result is not None
            assert os.path.exists(result)
            
            with open(result, 'r') as f:
                content = f.read()
                assert "Test content" in content
        finally:
            self.tearDown()
    
    def test_generate_leave_letter(self):
        """Test generating a leave letter"""
        self.setUp()
        try:
            result = self.controller.generate_leave_letter("health reasons", "2024-07-08")
            assert result is not None
            # The result should be a file path
            assert isinstance(result, str)
        finally:
            self.tearDown()

class TestConfirmationManager:
    """Test Confirmation Manager functionality"""
    
    def test_confirmation_manager_init(self):
        """Test confirmation manager initialization"""
        manager = ConfirmationManager()
        assert manager.root is not None
    
    @patch('config.REQUIRE_CONFIRMATION', False)
    def test_confirmation_bypassed(self):
        """Test confirmation bypass when disabled"""
        manager = ConfirmationManager()
        result = manager.confirm_action("Test action")
        assert result == True
    
    def test_sensitive_action_confirmation(self):
        """Test sensitive action confirmation"""
        manager = ConfirmationManager()
        # This will use mock in real test
        with patch.object(manager, '_confirm_gui', return_value=True):
            result = manager.confirm_sensitive_action("Delete all files")
            assert result == True

class TestTaskManager:
    """Test Task Manager functionality"""
    
    def test_task_manager_init(self):
        """Test task manager initialization"""
        manager = TaskManager()
        assert manager.tasks == {}
        assert manager.current_task is None
        assert manager.task_counter == 0
    
    def test_create_task(self):
        """Test creating a task"""
        manager = TaskManager()
        task = manager.create_task("Test Task", "Test description")
        assert task is not None
        assert task.name == "Test Task"
        assert task.description == "Test description"
        assert task.status == TaskStatus.PENDING
        assert task.id in manager.tasks
    
    def test_add_step(self):
        """Test adding a step to a task"""
        manager = TaskManager()
        task = manager.create_task("Test Task", "Test description")
        
        success = manager.add_step(
            task.id, 
            "Test step", 
            "test_action", 
            {"param": "value"}
        )
        assert success == True
        assert len(task.steps) == 1
        assert task.steps[0].description == "Test step"
    
    def test_get_task_progress(self):
        """Test getting task progress"""
        manager = TaskManager()
        task = manager.create_task("Test Task", "Test description")
        
        progress = manager.get_task_progress(task.id)
        assert progress['task_id'] == task.id
        assert progress['name'] == "Test Task"
        assert progress['status'] == TaskStatus.PENDING.value
        assert progress['total_steps'] == 0
        assert progress['completed_steps'] == 0
    
    def test_cancel_task(self):
        """Test cancelling a task"""
        manager = TaskManager()
        task = manager.create_task("Test Task", "Test description")
        
        success = manager.cancel_task(task.id)
        assert success == True
        assert task.status == TaskStatus.CANCELLED
    
    def test_list_tasks(self):
        """Test listing tasks"""
        manager = TaskManager()
        task1 = manager.create_task("Task 1", "Description 1")
        task2 = manager.create_task("Task 2", "Description 2")
        
        tasks = manager.list_tasks()
        assert len(tasks) == 2
        assert any(t['name'] == 'Task 1' for t in tasks)
        assert any(t['name'] == 'Task 2' for t in tasks)

class TestLogging:
    """Test logging functionality"""
    
    def test_setup_logging(self):
        """Test logging setup"""
        setup_logging()
        import logging
        
        # Test that logging is configured
        logger = logging.getLogger()
        assert logger.level == logging.INFO
        assert len(logger.handlers) >= 1

class TestConfig:
    """Test configuration"""
    
    def test_config_paths(self):
        """Test configuration paths"""
        assert os.path.exists(DESKTOP_PATH) or DESKTOP_PATH.endswith('Desktop')
        assert os.path.exists(DOCUMENTS_PATH) or DOCUMENTS_PATH.endswith('Documents')
    
    def test_config_imports(self):
        """Test that config imports work"""
        from config import (
            DEFAULT_LLM_PROVIDER, 
            VOICE_ENABLED, 
            REQUIRE_CONFIRMATION,
            BROWSER_TIMEOUT
        )
        assert DEFAULT_LLM_PROVIDER in ['openai', 'gemini', 'ollama']
        assert isinstance(VOICE_ENABLED, bool)
        assert isinstance(REQUIRE_CONFIRMATION, bool)
        assert isinstance(BROWSER_TIMEOUT, int)

class TestIntegration:
    """Integration tests"""
    
    def test_main_imports(self):
        """Test that main module imports work"""
        from main import ShadowAI
        shadow = ShadowAI()
        assert shadow is not None
        assert hasattr(shadow, 'run_interactive')
        assert hasattr(shadow, 'process_ai_command')
    
    def test_command_processing_flow(self):
        """Test the complete command processing flow"""
        # Test simple command
        result = process_command("open notepad")
        assert result['task_type'] == 'desktop_control'
        assert result['action'] == 'open_notepad'
        
        # Test type command
        result = process_command("type: Hello World")
        assert result['task_type'] == 'desktop_control'
        assert result['action'] == 'type_text'
        assert result['parameters']['text'] == 'Hello World'

# Fixtures
@pytest.fixture
def temp_directory():
    """Create a temporary directory for tests"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_desktop_controller():
    """Mock desktop controller"""
    with patch('control.desktop.DesktopController') as mock:
        yield mock

@pytest.fixture
def mock_document_controller():
    """Mock document controller"""
    with patch('control.documents.DocumentController') as mock:
        yield mock

# Test data
TEST_COMMANDS = [
    "open notepad",
    "type: Hello World",
    "click at 100, 200",
    "take a screenshot",
    "open calculator",
    "unknown command"
]

@pytest.mark.parametrize("command", TEST_COMMANDS)
def test_command_processing(command):
    """Test processing various commands"""
    result = process_command(command)
    assert 'task_type' in result
    assert 'action' in result
    assert 'parameters' in result
    assert 'confirmation_required' in result
    assert 'description' in result

# Performance tests
class TestPerformance:
    """Performance tests"""
    
    def test_command_processing_speed(self):
        """Test command processing speed"""
        import time
        
        start_time = time.time()
        for _ in range(100):
            process_command("open notepad")
        end_time = time.time()
        
        # Should process 100 commands in less than 1 second
        assert (end_time - start_time) < 1.0
    
    def test_task_creation_speed(self):
        """Test task creation speed"""
        import time
        
        manager = TaskManager()
        start_time = time.time()
        
        for i in range(100):
            manager.create_task(f"Task {i}", f"Description {i}")
        
        end_time = time.time()
        
        # Should create 100 tasks in less than 1 second
        assert (end_time - start_time) < 1.0

# Error handling tests
class TestErrorHandling:
    """Test error handling"""
    
    def test_invalid_coordinates(self):
        """Test handling of invalid coordinates"""
        controller = DesktopController()
        result = controller.click_at(-1, -1)
        assert result == False
    
    def test_empty_command(self):
        """Test handling of empty commands"""
        result = process_command("")
        assert result['task_type'] == 'unknown'
    
    def test_invalid_task_id(self):
        """Test handling of invalid task IDs"""
        manager = TaskManager()
        result = manager.cancel_task("invalid_id")
        assert result == False

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
