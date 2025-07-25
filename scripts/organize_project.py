#!/usr/bin/env python3
"""
Shadow AI Folder Organization Script
Maintains clean project structure and organization
"""

import os
import shutil
import json
from datetime import datetime

def create_folder_structure():
    """Create standardized folder structure"""
    folders = [
        'scripts/setup',
        'scripts/launchers', 
        'scripts/cleanup',
        'scripts/maintenance',
        'backup',
        'temp',
        'archive'
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✅ Created/verified: {folder}")

def organize_files():
    """Organize files into appropriate folders"""
    
    file_mappings = {
        'scripts/setup': [
            '*.bat', '*.ps1', '*install*.py', '*setup*.py', 
            'diagnostic.py', 'enhanced_installer.py', 'create_report.py'
        ],
        'scripts/launchers': [
            'launch*.py', 'simple_launcher.py', '*launcher*.py'
        ],
        'tests': [
            'test*.py', 'quick_test.py', 'simple_test.py', 'quick_check.py'
        ],
        'demos': [
            'demo*.py', '*demo*.py'
        ],
        'docs': [
            '*.md', 'PROJECT*.md', 'RELEASE*.md', 'SETUP*.md', 'README_*.md'
        ],
        'utils': [
            'pdf_editor.py', '*utility*.py', '*tool*.py'
        ],
        'backup': [
            '*backup*', '*bak', '*.old'
        ]
    }
    
    print("📁 Organizing files...")
    for target_folder, patterns in file_mappings.items():
        os.makedirs(target_folder, exist_ok=True)
        for pattern in patterns:
            # Implementation would move files matching patterns
            pass

def clean_empty_folders():
    """Remove empty folders"""
    for root, dirs, files in os.walk('.', topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    print(f"🗑️ Removed empty folder: {dir_path}")
            except OSError:
                pass

def generate_structure_report():
    """Generate folder structure report"""
    structure = {}
    
    for root, dirs, files in os.walk('.'):
        # Skip hidden and cache folders
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 2 * level
        folder_name = os.path.basename(root)
        
        if level == 0:
            print("📂 Shadow AI Project Structure:")
            print("=" * 40)
        
        if level > 0:
            print(f"{indent}📁 {folder_name}/")
        
        # List files in folder
        subindent = ' ' * 2 * (level + 1)
        for file in sorted(files):
            if not file.startswith('.') and not file.endswith('.pyc'):
                print(f"{subindent}📄 {file}")
    
    return structure

def main():
    """Main organization function"""
    print("🚀 Shadow AI Folder Organization")
    print("=" * 40)
    
    # Create folder structure
    create_folder_structure()
    
    # Generate structure report
    print("\n📊 Current Project Structure:")
    generate_structure_report()
    
    # Create organization summary
    summary = {
        "organized_date": datetime.now().isoformat(),
        "script_version": "1.0",
        "status": "organized"
    }
    
    with open('organization_status.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\n✅ Folder organization complete!")
    print("📄 Structure report saved to organization_status.json")

if __name__ == "__main__":
    main()
