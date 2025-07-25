#!/usr/bin/env python3
"""
Enhanced File Management Module for Shadow AI
Provides comprehensive file operations, organization, and management
"""

import os
import shutil
import glob
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import logging

class EnhancedFileManager:
    """Advanced file management with intelligent operations"""
    
    def __init__(self):
        self.operation_log = []
        self.common_paths = {
            'desktop': os.path.join(os.path.expanduser('~'), 'Desktop'),
            'documents': os.path.join(os.path.expanduser('~'), 'Documents'),
            'downloads': os.path.join(os.path.expanduser('~'), 'Downloads'),
            'pictures': os.path.join(os.path.expanduser('~'), 'Pictures'),
            'videos': os.path.join(os.path.expanduser('~'), 'Videos'),
            'music': os.path.join(os.path.expanduser('~'), 'Music'),
            'temp': os.environ.get('TEMP', 'C:\\Temp')
        }
        
    def copy_file(self, source: str, destination: str, overwrite: bool = False) -> bool:
        """Copy file with advanced options"""
        try:
            source_path = Path(source)
            dest_path = Path(destination)
            
            if not source_path.exists():
                logging.error(f"Source file not found: {source}")
                return False
                
            # Create destination directory if needed
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            if dest_path.exists() and not overwrite:
                logging.warning(f"Destination exists and overwrite=False: {destination}")
                return False
                
            shutil.copy2(source, destination)
            self.log_operation("copy", source, destination)
            logging.info(f"Copied: {source} -> {destination}")
            return True
            
        except Exception as e:
            logging.error(f"Error copying file: {e}")
            return False
    
    def move_file(self, source: str, destination: str, overwrite: bool = False) -> bool:
        """Move file with advanced options"""
        try:
            source_path = Path(source)
            dest_path = Path(destination)
            
            if not source_path.exists():
                logging.error(f"Source file not found: {source}")
                return False
                
            # Create destination directory if needed
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            if dest_path.exists() and not overwrite:
                logging.warning(f"Destination exists and overwrite=False: {destination}")
                return False
                
            shutil.move(source, destination)
            self.log_operation("move", source, destination)
            logging.info(f"Moved: {source} -> {destination}")
            return True
            
        except Exception as e:
            logging.error(f"Error moving file: {e}")
            return False
    
    def delete_file(self, filepath: str, permanent: bool = False) -> bool:
        """Delete file (to recycle bin or permanently)"""
        try:
            file_path = Path(filepath)
            
            if not file_path.exists():
                logging.error(f"File not found: {filepath}")
                return False
            
            if permanent:
                if file_path.is_file():
                    file_path.unlink()
                elif file_path.is_dir():
                    shutil.rmtree(filepath)
            else:
                # Try to use Windows recycle bin
                try:
                    import send2trash
                    send2trash.send2trash(filepath)
                except ImportError:
                    # Fallback to permanent deletion if send2trash not available
                    if file_path.is_file():
                        file_path.unlink()
                    elif file_path.is_dir():
                        shutil.rmtree(filepath)
            
            self.log_operation("delete", filepath, "")
            logging.info(f"Deleted: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Error deleting file: {e}")
            return False
    
    def rename_file(self, old_path: str, new_name: str) -> bool:
        """Rename file or folder"""
        try:
            old_file = Path(old_path)
            
            if not old_file.exists():
                logging.error(f"File not found: {old_path}")
                return False
            
            new_path = old_file.parent / new_name
            old_file.rename(new_path)
            
            self.log_operation("rename", old_path, str(new_path))
            logging.info(f"Renamed: {old_path} -> {new_path}")
            return True
            
        except Exception as e:
            logging.error(f"Error renaming file: {e}")
            return False
    
    def organize_by_type(self, folder_path: str, create_subfolders: bool = True) -> Dict[str, int]:
        """Organize files in folder by type"""
        try:
            folder = Path(folder_path)
            if not folder.exists():
                logging.error(f"Folder not found: {folder_path}")
                return {}
            
            file_types = {
                'Documents': ['.txt', '.doc', '.docx', '.pdf', '.rtf', '.odt'],
                'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
                'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
                'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
                'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
                'Spreadsheets': ['.xls', '.xlsx', '.csv', '.ods'],
                'Presentations': ['.ppt', '.pptx', '.odp'],
                'Code': ['.py', '.js', '.html', '.css', '.cpp', '.java', '.cs', '.php'],
                'Executables': ['.exe', '.msi', '.dmg', '.deb', '.rpm']
            }
            
            organized_count = {}
            
            for file_path in folder.iterdir():
                if file_path.is_file():
                    file_ext = file_path.suffix.lower()
                    
                    # Find appropriate category
                    category = None
                    for cat, extensions in file_types.items():
                        if file_ext in extensions:
                            category = cat
                            break
                    
                    if not category:
                        category = 'Others'
                    
                    # Create subfolder if needed
                    if create_subfolders:
                        category_folder = folder / category
                        category_folder.mkdir(exist_ok=True)
                        
                        # Move file to category folder
                        new_path = category_folder / file_path.name
                        if not new_path.exists():
                            file_path.rename(new_path)
                            organized_count[category] = organized_count.get(category, 0) + 1
            
            self.log_operation("organize", folder_path, f"Organized into {len(organized_count)} categories")
            return organized_count
            
        except Exception as e:
            logging.error(f"Error organizing folder: {e}")
            return {}
    
    def find_files(self, pattern: str, search_path: str = None, max_results: int = 100) -> List[str]:
        """Find files matching pattern"""
        try:
            if search_path is None:
                search_path = os.path.expanduser('~')
            
            search_path = Path(search_path)
            results = []
            
            # Use glob pattern matching
            for file_path in search_path.rglob(pattern):
                if file_path.is_file():
                    results.append(str(file_path))
                    if len(results) >= max_results:
                        break
            
            logging.info(f"Found {len(results)} files matching '{pattern}'")
            return results
            
        except Exception as e:
            logging.error(f"Error finding files: {e}")
            return []
    
    def find_large_files(self, folder_path: str, min_size_mb: int = 100) -> List[Tuple[str, int]]:
        """Find files larger than specified size"""
        try:
            folder = Path(folder_path)
            large_files = []
            min_size_bytes = min_size_mb * 1024 * 1024
            
            for file_path in folder.rglob('*'):
                if file_path.is_file():
                    try:
                        size = file_path.stat().st_size
                        if size >= min_size_bytes:
                            large_files.append((str(file_path), size // (1024 * 1024)))
                    except OSError:
                        continue
            
            # Sort by size (largest first)
            large_files.sort(key=lambda x: x[1], reverse=True)
            
            logging.info(f"Found {len(large_files)} files larger than {min_size_mb}MB")
            return large_files
            
        except Exception as e:
            logging.error(f"Error finding large files: {e}")
            return []
    
    def find_duplicate_files(self, folder_path: str) -> Dict[str, List[str]]:
        """Find duplicate files based on size and name"""
        try:
            folder = Path(folder_path)
            file_info = {}
            duplicates = {}
            
            for file_path in folder.rglob('*'):
                if file_path.is_file():
                    try:
                        size = file_path.stat().st_size
                        name = file_path.name.lower()
                        key = f"{name}_{size}"
                        
                        if key not in file_info:
                            file_info[key] = []
                        file_info[key].append(str(file_path))
                    except OSError:
                        continue
            
            # Find duplicates
            for key, paths in file_info.items():
                if len(paths) > 1:
                    duplicates[key] = paths
            
            logging.info(f"Found {len(duplicates)} sets of duplicate files")
            return duplicates
            
        except Exception as e:
            logging.error(f"Error finding duplicates: {e}")
            return {}
    
    def clean_temp_files(self, older_than_days: int = 7) -> int:
        """Clean temporary files older than specified days"""
        try:
            temp_paths = [
                self.common_paths['temp'],
                os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Temp'),
                'C:\\Windows\\Temp'
            ]
            
            cutoff_date = datetime.now() - timedelta(days=older_than_days)
            cleaned_count = 0
            
            for temp_path in temp_paths:
                if os.path.exists(temp_path):
                    try:
                        for file_path in Path(temp_path).rglob('*'):
                            if file_path.is_file():
                                try:
                                    file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                                    if file_time < cutoff_date:
                                        file_path.unlink()
                                        cleaned_count += 1
                                except (OSError, PermissionError):
                                    continue
                    except PermissionError:
                        continue
            
            self.log_operation("clean_temp", "", f"Cleaned {cleaned_count} files")
            logging.info(f"Cleaned {cleaned_count} temporary files")
            return cleaned_count
            
        except Exception as e:
            logging.error(f"Error cleaning temp files: {e}")
            return 0
    
    def create_backup(self, source_path: str, backup_location: str = None) -> bool:
        """Create backup of files/folders"""
        try:
            source = Path(source_path)
            
            if not source.exists():
                logging.error(f"Source not found: {source_path}")
                return False
            
            if backup_location is None:
                backup_location = self.common_paths['documents']
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{source.name}_backup_{timestamp}"
            backup_path = Path(backup_location) / backup_name
            
            if source.is_file():
                shutil.copy2(source_path, backup_path)
            else:
                shutil.copytree(source_path, backup_path)
            
            self.log_operation("backup", source_path, str(backup_path))
            logging.info(f"Backup created: {backup_path}")
            return True
            
        except Exception as e:
            logging.error(f"Error creating backup: {e}")
            return False
    
    def get_folder_info(self, folder_path: str) -> Dict:
        """Get detailed folder information"""
        try:
            folder = Path(folder_path)
            
            if not folder.exists():
                return {"error": "Folder not found"}
            
            total_size = 0
            file_count = 0
            folder_count = 0
            file_types = {}
            
            for item in folder.rglob('*'):
                if item.is_file():
                    file_count += 1
                    try:
                        size = item.stat().st_size
                        total_size += size
                        
                        ext = item.suffix.lower()
                        if ext:
                            file_types[ext] = file_types.get(ext, 0) + 1
                    except OSError:
                        continue
                elif item.is_dir():
                    folder_count += 1
            
            return {
                "path": folder_path,
                "total_size_mb": total_size // (1024 * 1024),
                "file_count": file_count,
                "folder_count": folder_count,
                "file_types": file_types
            }
            
        except Exception as e:
            logging.error(f"Error getting folder info: {e}")
            return {"error": str(e)}
    
    def log_operation(self, operation: str, source: str, destination: str):
        """Log file operation"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "source": source,
            "destination": destination
        }
        self.operation_log.append(log_entry)
        
        # Keep only last 1000 operations
        if len(self.operation_log) > 1000:
            self.operation_log = self.operation_log[-1000:]
    
    def get_operation_history(self, count: int = 10) -> List[Dict]:
        """Get recent file operations"""
        return self.operation_log[-count:]

# Global instance
file_manager = EnhancedFileManager()
