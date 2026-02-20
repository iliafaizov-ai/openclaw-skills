#!/usr/bin/env python3
"""
Parse tasks from Obsidian vault
Finds uncompleted tasks, prioritizes them, extracts deadlines
"""

import re
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class Task:
    def __init__(self, text: str, source_file: str, line_number: int):
        self.text = text
        self.source_file = source_file
        self.line_number = line_number
        self.completed = False
        self.priority = self._extract_priority()
        self.deadline = self._extract_deadline()
        self.tags = self._extract_tags()
        self.estimated_minutes = self._extract_time_estimate()
        
    def _extract_priority(self) -> str:
        """Extract priority from tags or keywords"""
        text_lower = self.text.lower()
        if '#срочно' in text_lower or '#urgent' in text_lower or '❗' in self.text:
            return 'high'
        elif '#важно' in text_lower or '#important' in text_lower or '⭐' in self.text:
            return 'high'
        elif '#низкий' in text_lower or '#low' in text_lower:
            return 'low'
        return 'medium'
    
    def _extract_deadline(self) -> Optional[datetime]:
        """Extract deadline from formats: 📅 YYYY-MM-DD, до DD.MM, deadline: ..."""
        # Format: 📅 2026-02-25
        match = re.search(r'📅\s*(\d{4}-\d{2}-\d{2})', self.text)
        if match:
            return datetime.strptime(match.group(1), '%Y-%m-%d')
        
        # Format: до 25.02
        match = re.search(r'до\s+(\d{1,2})\.(\d{1,2})', self.text)
        if match:
            day, month = int(match.group(1)), int(match.group(2))
            year = datetime.now().year
            return datetime(year, month, day)
        
        # Format: deadline: 2026-02-25
        match = re.search(r'deadline:\s*(\d{4}-\d{2}-\d{2})', self.text, re.IGNORECASE)
        if match:
            return datetime.strptime(match.group(1), '%Y-%m-%d')
        
        return None
    
    def _extract_tags(self) -> List[str]:
        """Extract all #tags"""
        return re.findall(r'#(\w+)', self.text)
    
    def _extract_time_estimate(self) -> Optional[int]:
        """Extract time estimate: (30 мин), (2ч), (1h)"""
        # Format: (30 мин) or (30м)
        match = re.search(r'\((\d+)\s*(?:мин|м|min|m)\)', self.text, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        # Format: (2ч) or (2h)
        match = re.search(r'\((\d+)\s*(?:ч|ч\.|h)\)', self.text, re.IGNORECASE)
        if match:
            return int(match.group(1)) * 60
        
        return None
    
    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if self.deadline:
            return datetime.now() > self.deadline
        return False
    
    def days_until_deadline(self) -> Optional[int]:
        """Days until deadline"""
        if self.deadline:
            delta = self.deadline - datetime.now()
            return delta.days
        return None
    
    def to_dict(self) -> Dict:
        """Convert to dict for JSON serialization"""
        return {
            'text': self.text,
            'source_file': self.source_file,
            'line_number': self.line_number,
            'completed': self.completed,
            'priority': self.priority,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'tags': self.tags,
            'estimated_minutes': self.estimated_minutes,
            'overdue': self.is_overdue()
        }


def parse_markdown_tasks(file_path: Path) -> List[Task]:
    """Parse tasks from a markdown file"""
    tasks = []
    
    if not file_path.exists():
        return tasks
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for i, line in enumerate(lines, 1):
            # Uncompleted task: - [ ]
            if re.match(r'^\s*-\s+\[\s\]\s+', line):
                task_text = re.sub(r'^\s*-\s+\[\s\]\s+', '', line).strip()
                task = Task(task_text, str(file_path), i)
                tasks.append(task)
    
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    
    return tasks


def scan_vault_for_tasks(vault_path: str, sources: List[str]) -> List[Task]:
    """Scan vault directories for tasks"""
    vault = Path(vault_path)
    all_tasks = []
    
    for source in sources:
        source_path = vault / source
        
        if source_path.is_file():
            # Single file
            all_tasks.extend(parse_markdown_tasks(source_path))
        elif source_path.is_dir():
            # Directory - scan all .md files
            for md_file in source_path.rglob('*.md'):
                all_tasks.extend(parse_markdown_tasks(md_file))
    
    return all_tasks


def prioritize_tasks(tasks: List[Task], high_priority_keywords: List[str]) -> List[Task]:
    """Sort tasks by priority"""
    
    def task_score(task: Task) -> tuple:
        """Calculate priority score (lower = higher priority)"""
        # Priority level
        priority_score = {'high': 0, 'medium': 1, 'low': 2}[task.priority]
        
        # Deadline urgency
        if task.is_overdue():
            deadline_score = -1000  # Highest priority
        elif task.deadline:
            days = task.days_until_deadline()
            deadline_score = days if days is not None else 1000
        else:
            deadline_score = 1000  # No deadline = lower priority
        
        # High-priority project keywords
        keyword_score = 0
        for keyword in high_priority_keywords:
            if keyword.lower() in task.text.lower():
                keyword_score = -100
                break
        
        return (priority_score, deadline_score, keyword_score)
    
    return sorted(tasks, key=task_score)


def main():
    """Main entry point"""
    import sys
    
    # Load config
    config_path = Path(__file__).parent.parent / 'config.json'
    with open(config_path) as f:
        config = json.load(f)
    
    # Scan for tasks
    tasks = scan_vault_for_tasks(
        config['obsidian']['vault_path'],
        config['obsidian']['tasks_sources']
    )
    
    # Prioritize
    tasks = prioritize_tasks(
        tasks,
        config['priorities']['high_priority_projects']
    )
    
    # Limit to max tasks per day
    max_tasks = config['priorities']['max_tasks_per_day']
    tasks = tasks[:max_tasks]
    
    # Output as JSON
    output = {
        'total_found': len(tasks),
        'tasks': [t.to_dict() for t in tasks]
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
