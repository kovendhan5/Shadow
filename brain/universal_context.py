"""
Universal Context Manager for Shadow AI
Manages context, memory, and learning for the universal assistant
"""
import logging
import json
import sqlite3
import time
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
import os

@dataclass
class UserPreference:
    """User preference data"""
    category: str
    preference_key: str
    preference_value: str
    confidence: float
    last_updated: datetime

@dataclass
class TaskContext:
    """Context for a specific task"""
    task_id: str
    user_intent: str
    active_applications: List[str]
    current_screen_state: Dict[str, Any]
    file_system_state: Dict[str, Any]
    user_location: str
    time_context: Dict[str, Any]
    previous_tasks: List[str]

@dataclass
class ConversationContext:
    """Context for the current conversation"""
    session_id: str
    start_time: datetime
    user_queries: List[str]
    completed_tasks: List[str]
    current_focus: Optional[str]
    user_mood: Optional[str]
    interaction_mode: str  # voice, text, mixed

class UniversalContextManager:
    """
    Manages context, memory, and learning for Shadow AI
    """
    
    def __init__(self):
        self.setup_database()
        self.current_session = self._create_new_session()
        self.memory_cache = {}
        self.active_contexts = {}
        self.user_patterns = {}
        
    def setup_database(self):
        """Setup SQLite database for persistent memory"""
        self.db_path = Path.home() / ".shadow_ai" / "memory.db"
        self.db_path.parent.mkdir(exist_ok=True)
        
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                preference_key TEXT NOT NULL,
                preference_value TEXT NOT NULL,
                confidence REAL NOT NULL,
                last_updated TIMESTAMP NOT NULL,
                UNIQUE(category, preference_key)
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS task_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT UNIQUE NOT NULL,
                user_command TEXT NOT NULL,
                task_category TEXT NOT NULL,
                execution_time REAL NOT NULL,
                success BOOLEAN NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                context_data TEXT
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                user_query TEXT NOT NULL,
                response_summary TEXT,
                timestamp TIMESTAMP NOT NULL,
                success BOOLEAN NOT NULL
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS learning_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT NOT NULL,
                pattern_data TEXT NOT NULL,
                frequency INTEGER DEFAULT 1,
                last_seen TIMESTAMP NOT NULL,
                confidence REAL NOT NULL
            )
        ''')
        
        self.conn.commit()

    def _create_new_session(self) -> ConversationContext:
        """Create a new conversation session"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return ConversationContext(
            session_id=session_id,
            start_time=datetime.now(),
            user_queries=[],
            completed_tasks=[],
            current_focus=None,
            user_mood=None,
            interaction_mode="text"
        )

    def add_user_query(self, query: str, response_success: bool = True):
        """Add user query to conversation context"""
        self.current_session.user_queries.append(query)
        
        # Store in database
        self.conn.execute('''
            INSERT INTO conversation_history 
            (session_id, user_query, timestamp, success)
            VALUES (?, ?, ?, ?)
        ''', (self.current_session.session_id, query, datetime.now(), response_success))
        self.conn.commit()
        
        # Update patterns
        self._update_user_patterns(query)

    def add_completed_task(self, task_id: str, task_summary: str):
        """Add completed task to context"""
        self.current_session.completed_tasks.append(task_id)
        
        # Update focus based on task category
        self._update_current_focus(task_summary)

    def get_contextual_suggestions(self, current_query: str) -> List[str]:
        """Get contextual suggestions based on history and patterns"""
        suggestions = []
        
        # Based on recent tasks
        recent_tasks = self._get_recent_similar_tasks(current_query)
        suggestions.extend([f"Similar to: {task}" for task in recent_tasks[:3]])
        
        # Based on time patterns
        time_suggestions = self._get_time_based_suggestions()
        suggestions.extend(time_suggestions)
        
        # Based on user preferences
        pref_suggestions = self._get_preference_based_suggestions(current_query)
        suggestions.extend(pref_suggestions)
        
        return suggestions[:5]  # Limit to top 5

    def learn_user_preference(self, category: str, key: str, value: str, confidence: float = 0.8):
        """Learn and store user preference"""
        self.conn.execute('''
            INSERT OR REPLACE INTO user_preferences 
            (category, preference_key, preference_value, confidence, last_updated)
            VALUES (?, ?, ?, ?, ?)
        ''', (category, key, value, confidence, datetime.now()))
        self.conn.commit()

    def get_user_preference(self, category: str, key: str) -> Optional[str]:
        """Get user preference"""
        cursor = self.conn.execute('''
            SELECT preference_value FROM user_preferences 
            WHERE category = ? AND preference_key = ?
        ''', (category, key))
        
        result = cursor.fetchone()
        return result[0] if result else None

    def get_task_context(self, user_command: str) -> TaskContext:
        """Generate comprehensive task context"""
        return TaskContext(
            task_id=f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            user_intent=self._analyze_user_intent(user_command),
            active_applications=self._get_active_applications(),
            current_screen_state=self._get_screen_state(),
            file_system_state=self._get_file_system_state(),
            user_location=self._get_user_location(),
            time_context=self._get_time_context(),
            previous_tasks=self.current_session.completed_tasks[-5:]  # Last 5 tasks
        )

    def store_task_result(self, task_id: str, user_command: str, category: str, 
                         execution_time: float, success: bool, context_data: Dict[str, Any]):
        """Store task execution result for learning"""
        self.conn.execute('''
            INSERT INTO task_history 
            (task_id, user_command, task_category, execution_time, success, timestamp, context_data)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (task_id, user_command, category, execution_time, success, datetime.now(), 
              json.dumps(context_data)))
        self.conn.commit()

    def get_similar_tasks(self, current_command: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get similar tasks from history"""
        # Simple similarity based on keyword matching
        words = set(current_command.lower().split())
        
        cursor = self.conn.execute('''
            SELECT task_id, user_command, task_category, success, timestamp 
            FROM task_history 
            ORDER BY timestamp DESC 
            LIMIT 50
        ''')
        
        tasks = cursor.fetchall()
        similar_tasks = []
        
        for task in tasks:
            task_words = set(task[1].lower().split())
            similarity = len(words.intersection(task_words)) / len(words.union(task_words))
            
            if similarity > 0.3:  # 30% similarity threshold
                similar_tasks.append({
                    'task_id': task[0],
                    'command': task[1],
                    'category': task[2],
                    'success': task[3],
                    'timestamp': task[4],
                    'similarity': similarity
                })
        
        # Sort by similarity and return top results
        similar_tasks.sort(key=lambda x: x['similarity'], reverse=True)
        return similar_tasks[:limit]

    def get_user_statistics(self) -> Dict[str, Any]:
        """Get user usage statistics"""
        cursor = self.conn.execute('''
            SELECT 
                COUNT(*) as total_tasks,
                COUNT(CASE WHEN success = 1 THEN 1 END) as successful_tasks,
                AVG(execution_time) as avg_execution_time,
                task_category,
                COUNT(*) as category_count
            FROM task_history 
            GROUP BY task_category
        ''')
        
        stats = cursor.fetchall()
        
        total_cursor = self.conn.execute('SELECT COUNT(*) FROM task_history')
        total_tasks = total_cursor.fetchone()[0]
        
        success_cursor = self.conn.execute('SELECT COUNT(*) FROM task_history WHERE success = 1')
        successful_tasks = success_cursor.fetchone()[0]
        
        return {
            'total_tasks': total_tasks,
            'successful_tasks': successful_tasks,
            'success_rate': successful_tasks / total_tasks if total_tasks > 0 else 0,
            'category_breakdown': [
                {'category': row[3], 'count': row[4], 'avg_time': row[2]}
                for row in stats
            ],
            'most_used_categories': sorted(
                [{'category': row[3], 'count': row[4]} for row in stats],
                key=lambda x: x['count'], reverse=True
            )[:5]
        }

    def _analyze_user_intent(self, command: str) -> str:
        """Analyze user intent from command"""
        command_lower = command.lower()
        
        if any(word in command_lower for word in ['create', 'write', 'generate', 'make']):
            return 'creation'
        elif any(word in command_lower for word in ['open', 'launch', 'start', 'run']):
            return 'application_control'
        elif any(word in command_lower for word in ['search', 'find', 'look', 'browse']):
            return 'information_retrieval'
        elif any(word in command_lower for word in ['send', 'email', 'message', 'share']):
            return 'communication'
        elif any(word in command_lower for word in ['organize', 'clean', 'sort', 'arrange']):
            return 'organization'
        elif any(word in command_lower for word in ['help', 'how', 'what', 'explain']):
            return 'assistance'
        else:
            return 'general'

    def _get_active_applications(self) -> List[str]:
        """Get list of currently active applications"""
        try:
            import psutil
            active_apps = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'] and proc.info['name'].endswith('.exe'):
                        active_apps.append(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return list(set(active_apps))  # Remove duplicates
        except ImportError:
            return ["psutil_not_available"]

    def _get_screen_state(self) -> Dict[str, Any]:
        """Get current screen state information"""
        try:
            import pyautogui
            screen_size = pyautogui.size()
            return {
                'screen_width': screen_size.width,
                'screen_height': screen_size.height,
                'timestamp': datetime.now().isoformat()
            }
        except:
            return {'error': 'screen_state_unavailable'}

    def _get_file_system_state(self) -> Dict[str, Any]:
        """Get relevant file system state"""
        try:
            home_dir = Path.home()
            desktop_files = list(home_dir.glob('Desktop/*'))
            documents_files = list(home_dir.glob('Documents/*'))
            downloads_files = list(home_dir.glob('Downloads/*'))
            
            return {
                'desktop_file_count': len(desktop_files),
                'documents_file_count': len(documents_files),
                'downloads_file_count': len(downloads_files),
                'home_directory': str(home_dir),
                'recent_files': [str(f) for f in sorted(
                    desktop_files + documents_files + downloads_files,
                    key=lambda x: x.stat().st_mtime, reverse=True
                )[:10]]
            }
        except:
            return {'error': 'filesystem_state_unavailable'}

    def _get_user_location(self) -> str:
        """Get user location context (timezone-based)"""
        try:
            import time
            timezone = time.tzname[0]
            return f"timezone_{timezone}"
        except:
            return "location_unknown"

    def _get_time_context(self) -> Dict[str, Any]:
        """Get time-based context"""
        now = datetime.now()
        return {
            'hour': now.hour,
            'day_of_week': now.weekday(),
            'is_weekend': now.weekday() >= 5,
            'is_work_hours': 9 <= now.hour <= 17,
            'time_of_day': self._get_time_of_day(now.hour)
        }

    def _get_time_of_day(self, hour: int) -> str:
        """Get time of day category"""
        if 5 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 17:
            return 'afternoon'
        elif 17 <= hour < 21:
            return 'evening'
        else:
            return 'night'

    def _update_user_patterns(self, query: str):
        """Update user behavior patterns"""
        # Extract patterns from query
        words = query.lower().split()
        time_context = self._get_time_context()
        
        # Time-based patterns
        pattern_data = {
            'words': words,
            'hour': time_context['hour'],
            'time_of_day': time_context['time_of_day'],
            'is_weekend': time_context['is_weekend']
        }
        
        pattern_key = f"time_pattern_{time_context['time_of_day']}"
        self._store_pattern('temporal', pattern_key, pattern_data)
        
        # Word frequency patterns
        for word in words:
            if len(word) > 2:  # Skip short words
                self._store_pattern('word_frequency', word, {'count': 1})

    def _store_pattern(self, pattern_type: str, pattern_key: str, pattern_data: Dict[str, Any]):
        """Store a learned pattern"""
        pattern_json = json.dumps(pattern_data)
        
        # Check if pattern exists
        cursor = self.conn.execute('''
            SELECT frequency FROM learning_patterns 
            WHERE pattern_type = ? AND pattern_data LIKE ?
        ''', (pattern_type, f'%{pattern_key}%'))
        
        result = cursor.fetchone()
        
        if result:
            # Update frequency
            self.conn.execute('''
                UPDATE learning_patterns 
                SET frequency = frequency + 1, last_seen = ?
                WHERE pattern_type = ? AND pattern_data LIKE ?
            ''', (datetime.now(), pattern_type, f'%{pattern_key}%'))
        else:
            # Insert new pattern
            self.conn.execute('''
                INSERT INTO learning_patterns 
                (pattern_type, pattern_data, frequency, last_seen, confidence)
                VALUES (?, ?, 1, ?, 0.5)
            ''', (pattern_type, pattern_json, datetime.now()))
        
        self.conn.commit()

    def _update_current_focus(self, task_summary: str):
        """Update current user focus based on completed tasks"""
        # Simple focus detection based on recent task categories
        if any(word in task_summary.lower() for word in ['document', 'write', 'create']):
            self.current_session.current_focus = 'document_creation'
        elif any(word in task_summary.lower() for word in ['web', 'search', 'browse']):
            self.current_session.current_focus = 'web_research'
        elif any(word in task_summary.lower() for word in ['email', 'message', 'send']):
            self.current_session.current_focus = 'communication'
        elif any(word in task_summary.lower() for word in ['file', 'organize', 'folder']):
            self.current_session.current_focus = 'file_management'

    def _get_recent_similar_tasks(self, query: str) -> List[str]:
        """Get recent similar tasks"""
        similar_tasks = self.get_similar_tasks(query, 3)
        return [task['command'] for task in similar_tasks]

    def _get_time_based_suggestions(self) -> List[str]:
        """Get suggestions based on time patterns"""
        time_context = self._get_time_context()
        suggestions = []
        
        if time_context['time_of_day'] == 'morning':
            suggestions.append("Check your calendar for today")
            suggestions.append("Review your daily tasks")
        elif time_context['time_of_day'] == 'evening':
            suggestions.append("Organize today's work files")
            suggestions.append("Prepare tomorrow's schedule")
        
        if time_context['is_weekend']:
            suggestions.append("Organize personal files")
            suggestions.append("Back up important documents")
        
        return suggestions

    def _get_preference_based_suggestions(self, query: str) -> List[str]:
        """Get suggestions based on user preferences"""
        # This would analyze user preferences and suggest relevant actions
        return []

    def cleanup_old_data(self, days_to_keep: int = 90):
        """Clean up old data to maintain performance"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        # Clean old conversation history
        self.conn.execute('''
            DELETE FROM conversation_history 
            WHERE timestamp < ?
        ''', (cutoff_date,))
        
        # Clean old task history (keep successful tasks longer)
        self.conn.execute('''
            DELETE FROM task_history 
            WHERE timestamp < ? AND success = 0
        ''', (cutoff_date,))
        
        # Clean old patterns with low frequency
        self.conn.execute('''
            DELETE FROM learning_patterns 
            WHERE last_seen < ? AND frequency < 3
        ''', (cutoff_date,))
        
        self.conn.commit()

    def close(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

# Global instance
context_manager = UniversalContextManager()

def get_task_context(user_command: str) -> TaskContext:
    """Get task context for a user command"""
    return context_manager.get_task_context(user_command)

def learn_from_task(task_id: str, user_command: str, category: str, 
                   execution_time: float, success: bool, context_data: Dict[str, Any]):
    """Learn from task execution"""
    context_manager.store_task_result(task_id, user_command, category, execution_time, success, context_data)
    context_manager.add_completed_task(task_id, user_command)

def add_user_interaction(query: str, success: bool = True):
    """Add user interaction to context"""
    context_manager.add_user_query(query, success)
