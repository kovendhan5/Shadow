# web_interface.py
"""
Shadow AI Web Interface
A simple web interface for Shadow AI using Flask
"""

try:
    from flask import Flask, render_template, request, jsonify, send_from_directory
    from flask_socketio import SocketIO, emit
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

import os
import json
import logging
import threading
import time
from datetime import datetime
from main import ShadowAI
from task_manager import task_manager

if FLASK_AVAILABLE:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'shadow-ai-secret-key'
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # Global Shadow AI instance
    shadow_ai = ShadowAI()
    
    @app.route('/')
    def index():
        """Main page"""
        return render_template('index.html')
    
    @app.route('/api/execute', methods=['POST'])
    def execute_command():
        """Execute a command"""
        try:
            data = request.json
            command = data.get('command', '').strip()
            
            if not command:
                return jsonify({'error': 'No command provided'}), 400
            
            # Execute command in background
            thread = threading.Thread(target=execute_command_async, args=(command,))
            thread.daemon = True
            thread.start()
            
            return jsonify({'message': 'Command accepted', 'status': 'processing'})
        
        except Exception as e:
            logging.error(f"Error executing command: {e}")
            return jsonify({'error': str(e)}), 500
    
    def execute_command_async(command):
        """Execute command asynchronously"""
        try:
            socketio.emit('command_started', {'command': command})
            success = shadow_ai.run_single_command(command)
            socketio.emit('command_completed', {'success': success, 'command': command})
        except Exception as e:
            logging.error(f"Error in async command: {e}")
            socketio.emit('command_error', {'error': str(e), 'command': command})
    
    @app.route('/api/tasks')
    def get_tasks():
        """Get all tasks"""
        tasks = task_manager.list_tasks()
        return jsonify(tasks)
    
    @app.route('/api/tasks/<task_id>')
    def get_task(task_id):
        """Get specific task details"""
        progress = task_manager.get_task_progress(task_id)
        if progress:
            return jsonify(progress)
        return jsonify({'error': 'Task not found'}), 404
    
    @app.route('/api/tasks/<task_id>/cancel', methods=['POST'])
    def cancel_task(task_id):
        """Cancel a task"""
        success = task_manager.cancel_task(task_id)
        if success:
            return jsonify({'message': 'Task cancelled'})
        return jsonify({'error': 'Task not found'}), 404
    
    @app.route('/api/status')
    def get_status():
        """Get system status"""
        return jsonify({
            'status': 'running',
            'tasks_count': len(task_manager.list_tasks()),
            'timestamp': datetime.now().isoformat()
        })
    
    @app.route('/api/logs')
    def get_logs():
        """Get recent logs"""
        try:
            log_file = "logs/shadow.log"
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    # Return last 100 lines
                    recent_logs = lines[-100:] if len(lines) > 100 else lines
                    return jsonify({'logs': recent_logs})
            return jsonify({'logs': []})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection"""
        emit('connected', {'message': 'Connected to Shadow AI'})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        logging.info('Client disconnected')
    
    @socketio.on('execute_command')
    def handle_execute_command(data):
        """Handle command execution via WebSocket"""
        command = data.get('command', '').strip()
        if command:
            thread = threading.Thread(target=execute_command_async, args=(command,))
            thread.daemon = True
            thread.start()
    
    # Create templates directory and HTML template
    def create_html_template():
        """Create HTML template for web interface"""
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        os.makedirs(templates_dir, exist_ok=True)
        
        html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🧠 Shadow AI Agent</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                padding: 30px;
                text-align: center;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .header p {
                font-size: 1.2em;
                opacity: 0.9;
            }
            
            .main-content {
                padding: 30px;
            }
            
            .command-section {
                background: #f8f9fa;
                padding: 25px;
                border-radius: 10px;
                margin-bottom: 30px;
            }
            
            .command-input {
                display: flex;
                gap: 15px;
                margin-bottom: 20px;
            }
            
            #commandInput {
                flex: 1;
                padding: 15px;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.3s;
            }
            
            #commandInput:focus {
                outline: none;
                border-color: #667eea;
            }
            
            .btn {
                padding: 15px 25px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .btn-primary {
                background: #667eea;
                color: white;
            }
            
            .btn-primary:hover {
                background: #5a6fd8;
                transform: translateY(-2px);
            }
            
            .btn-secondary {
                background: #6c757d;
                color: white;
            }
            
            .btn-secondary:hover {
                background: #5a6268;
            }
            
            .tabs {
                display: flex;
                margin-bottom: 20px;
                border-bottom: 2px solid #eee;
            }
            
            .tab {
                padding: 15px 25px;
                cursor: pointer;
                border: none;
                background: none;
                font-size: 16px;
                transition: all 0.3s;
            }
            
            .tab.active {
                background: #667eea;
                color: white;
                border-radius: 8px 8px 0 0;
            }
            
            .tab-content {
                display: none;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 0 10px 10px 10px;
                min-height: 400px;
            }
            
            .tab-content.active {
                display: block;
            }
            
            .output-area {
                background: #1a1a1a;
                color: #00ff00;
                padding: 20px;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                height: 300px;
                overflow-y: auto;
                font-size: 14px;
                line-height: 1.4;
            }
            
            .task-list {
                max-height: 400px;
                overflow-y: auto;
            }
            
            .task-item {
                background: white;
                padding: 15px;
                margin-bottom: 10px;
                border-radius: 8px;
                border-left: 4px solid #667eea;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            
            .task-status {
                display: inline-block;
                padding: 5px 10px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: bold;
                text-transform: uppercase;
            }
            
            .status-pending { background: #ffc107; color: #212529; }
            .status-running { background: #17a2b8; color: white; }
            .status-completed { background: #28a745; color: white; }
            .status-failed { background: #dc3545; color: white; }
            
            .examples {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }
            
            .example-card {
                background: white;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #28a745;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .example-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            
            .example-card h4 {
                color: #667eea;
                margin-bottom: 10px;
            }
            
            .status-bar {
                background: #333;
                color: white;
                padding: 10px 20px;
                font-size: 14px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .spinner {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🧠 Shadow AI Agent</h1>
                <p>Your Personal AI Assistant for Windows</p>
            </div>
            
            <div class="main-content">
                <div class="command-section">
                    <h3>Command Input</h3>
                    <div class="command-input">
                        <input type="text" id="commandInput" placeholder="Type your command here... (e.g., 'open notepad', 'write a leave letter')" />
                        <button class="btn btn-primary" onclick="executeCommand()">Execute</button>
                        <button class="btn btn-secondary" onclick="clearCommand()">Clear</button>
                    </div>
                </div>
                
                <div class="tabs">
                    <button class="tab active" onclick="showTab('output')">Output</button>
                    <button class="tab" onclick="showTab('tasks')">Tasks</button>
                    <button class="tab" onclick="showTab('examples')">Examples</button>
                </div>
                
                <div id="output" class="tab-content active">
                    <h3>Output</h3>
                    <div id="outputArea" class="output-area">
                        <div>🧠 Shadow AI Agent initialized and ready for commands...</div>
                        <div>Type a command above and press Execute to get started!</div>
                    </div>
                </div>
                
                <div id="tasks" class="tab-content">
                    <h3>Tasks</h3>
                    <div style="margin-bottom: 15px;">
                        <button class="btn btn-secondary" onclick="refreshTasks()">Refresh Tasks</button>
                    </div>
                    <div id="tasksList" class="task-list">
                        <!-- Tasks will be loaded here -->
                    </div>
                </div>
                
                <div id="examples" class="tab-content">
                    <h3>Example Commands</h3>
                    <div class="examples">
                        <div class="example-card" onclick="setCommand('open notepad')">
                            <h4>Open Applications</h4>
                            <p>Open notepad, calculator, or any application</p>
                        </div>
                        <div class="example-card" onclick="setCommand('write a leave letter for tomorrow')">
                            <h4>Document Creation</h4>
                            <p>Generate letters, reports, and documents</p>
                        </div>
                        <div class="example-card" onclick="setCommand('search for iPhone on Flipkart')">
                            <h4>Web Automation</h4>
                            <p>Search products, browse websites</p>
                        </div>
                        <div class="example-card" onclick="setCommand('take a screenshot')">
                            <h4>Desktop Control</h4>
                            <p>Screenshots, clicks, typing</p>
                        </div>
                        <div class="example-card" onclick="setCommand('create a resume template')">
                            <h4>Professional Documents</h4>
                            <p>Resumes, cover letters, proposals</p>
                        </div>
                        <div class="example-card" onclick="setCommand('type: Hello World')">
                            <h4>Direct Actions</h4>
                            <p>Type text, click coordinates</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="status-bar">
                <span id="statusText">Ready</span>
                <span id="statusTime"></span>
            </div>
        </div>
        
        <script>
            const socket = io();
            const commandInput = document.getElementById('commandInput');
            const outputArea = document.getElementById('outputArea');
            
            // Socket event handlers
            socket.on('connected', function(data) {
                addToOutput('🟢 Connected to Shadow AI');
            });
            
            socket.on('command_started', function(data) {
                addToOutput('🤖 Processing: ' + data.command);
                setStatus('Processing command...', true);
            });
            
            socket.on('command_completed', function(data) {
                if (data.success) {
                    addToOutput('✅ Command completed successfully');
                } else {
                    addToOutput('❌ Command failed');
                }
                setStatus('Ready', false);
                refreshTasks();
            });
            
            socket.on('command_error', function(data) {
                addToOutput('❌ Error: ' + data.error);
                setStatus('Ready', false);
            });
            
            // Functions
            function executeCommand() {
                const command = commandInput.value.trim();
                if (!command) return;
                
                addToOutput('> ' + command);
                
                fetch('/api/execute', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ command: command })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        addToOutput('❌ Error: ' + data.error);
                    }
                })
                .catch(error => {
                    addToOutput('❌ Network error: ' + error.message);
                });
                
                commandInput.value = '';
            }
            
            function clearCommand() {
                commandInput.value = '';
                commandInput.focus();
            }
            
            function setCommand(command) {
                commandInput.value = command;
                commandInput.focus();
            }
            
            function addToOutput(text) {
                const timestamp = new Date().toLocaleTimeString();
                outputArea.innerHTML += '<div>[' + timestamp + '] ' + text + '</div>';
                outputArea.scrollTop = outputArea.scrollHeight;
            }
            
            function showTab(tabName) {
                // Hide all tabs
                const tabs = document.querySelectorAll('.tab');
                const contents = document.querySelectorAll('.tab-content');
                
                tabs.forEach(tab => tab.classList.remove('active'));
                contents.forEach(content => content.classList.remove('active'));
                
                // Show selected tab
                event.target.classList.add('active');
                document.getElementById(tabName).classList.add('active');
            }
            
            function refreshTasks() {
                fetch('/api/tasks')
                .then(response => response.json())
                .then(tasks => {
                    const tasksList = document.getElementById('tasksList');
                    tasksList.innerHTML = '';
                    
                    if (tasks.length === 0) {
                        tasksList.innerHTML = '<div style="text-align: center; color: #666;">No tasks found</div>';
                        return;
                    }
                    
                    tasks.forEach(task => {
                        const taskDiv = document.createElement('div');
                        taskDiv.className = 'task-item';
                        taskDiv.innerHTML = `
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <h4>${task.name}</h4>
                                    <p>${task.description}</p>
                                </div>
                                <span class="task-status status-${task.status}">${task.status}</span>
                            </div>
                        `;
                        tasksList.appendChild(taskDiv);
                    });
                })
                .catch(error => {
                    console.error('Error fetching tasks:', error);
                });
            }
            
            function setStatus(text, loading = false) {
                const statusText = document.getElementById('statusText');
                const statusTime = document.getElementById('statusTime');
                
                if (loading) {
                    statusText.innerHTML = '<span class="spinner"></span> ' + text;
                } else {
                    statusText.textContent = text;
                }
                
                statusTime.textContent = new Date().toLocaleTimeString();
            }
            
            // Event listeners
            commandInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    executeCommand();
                }
            });
            
            // Initialize
            document.addEventListener('DOMContentLoaded', function() {
                refreshTasks();
                setStatus('Ready', false);
                commandInput.focus();
            });
        </script>
    </body>
    </html>
        """
        
        template_path = os.path.join(templates_dir, 'index.html')
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logging.info(f"Created web template: {template_path}")
    
    def run_web_interface(host='127.0.0.1', port=5000, debug=False):
        """Run the web interface"""
        create_html_template()
        logging.info(f"Starting Shadow AI web interface on http://{host}:{port}")
        socketio.run(app, host=host, port=port, debug=debug)

else:
    def run_web_interface(*args, **kwargs):
        print("❌ Flask is not installed. Please install it with: pip install flask flask-socketio")
        print("Web interface is not available.")

if __name__ == "__main__":
    if FLASK_AVAILABLE:
        run_web_interface(debug=True)
    else:
        print("Flask is not available. Please install Flask and Flask-SocketIO to use the web interface.")
