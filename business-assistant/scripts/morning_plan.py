#!/usr/bin/env python3
"""
Generate morning daily plan
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

def get_calendar_events():
    """Get today's calendar events"""
    try:
        calendar_script = Path.home() / '.openclaw/workspace/calendar/list_events.js'
        if calendar_script.exists():
            result = subprocess.run(
                ['node', str(calendar_script)],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                # Parse output
                events = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        events.append(line.strip())
                return events
        return []
    except Exception as e:
        return [f"⚠️ Не удалось загрузить календарь: {e}"]


def get_tasks():
    """Get prioritized tasks from Obsidian"""
    try:
        parser_script = Path(__file__).parent / 'tasks_parser.py'
        result = subprocess.run(
            ['python3', str(parser_script)],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        return {'total_found': 0, 'tasks': []}
    except Exception as e:
        print(f"Error getting tasks: {e}")
        return {'total_found': 0, 'tasks': []}


def create_daily_file(date_str: str, template_path: Path, diary_path: Path):
    """Create daily file from template"""
    daily_file = diary_path / f"{date_str}.md"
    
    if daily_file.exists():
        return daily_file
    
    # Read template
    if template_path.exists():
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = f"# {date_str}\n\n## 📅 Календарь\n\n## 🎯 Задачи\n\n## 💡 Заметки\n\n"
    
    # Replace placeholders
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    weekday_ru = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    weekday = weekday_ru[date_obj.weekday()]
    
    content = content.replace('YYYY-MM-DD', date_str)
    content = content.replace('День недели', weekday)
    
    # Write file
    with open(daily_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return daily_file


def estimate_available_time(events: list) -> int:
    """Estimate available work time in minutes"""
    # Simple heuristic: 8 working hours - 1h per meeting
    total_minutes = 8 * 60  # 8 hours
    meetings = len([e for e in events if e and not e.startswith('⚠️')])
    meeting_time = meetings * 60  # Assume 1h per meeting
    
    return max(total_minutes - meeting_time, 0)


def format_plan(tasks_data: dict, events: list) -> str:
    """Format daily plan message"""
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    weekday_ru = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    weekday = weekday_ru[today.weekday()]
    
    plan = f"📅 **План дня ({today.strftime('%d.%m.%Y')}, {weekday})**\n\n"
    
    # Calendar
    if events:
        plan += "## 📆 Календарь:\n"
        for event in events:
            plan += f"- {event}\n"
        plan += "\n"
    
    # Tasks
    tasks = tasks_data.get('tasks', [])
    
    if tasks:
        # High priority / overdue
        urgent = [t for t in tasks if t.get('overdue') or t.get('priority') == 'high']
        if urgent:
            plan += "## 🔥 Срочные/важные:\n"
            for task in urgent:
                deadline = f" 📅 {task['deadline'][:10]}" if task.get('deadline') else ""
                plan += f"- [ ] {task['text']}{deadline}\n"
            plan += "\n"
        
        # Regular tasks
        regular = [t for t in tasks if not (t.get('overdue') or t.get('priority') == 'high')]
        if regular:
            plan += "## 📝 Задачи:\n"
            for task in regular[:5]:  # Top 5 regular tasks
                deadline = f" 📅 {task['deadline'][:10]}" if task.get('deadline') else ""
                time_est = f" ({task['estimated_minutes']}м)" if task.get('estimated_minutes') else ""
                plan += f"- [ ] {task['text']}{deadline}{time_est}\n"
            plan += "\n"
    
    # Time estimate
    available_minutes = estimate_available_time(events)
    available_hours = available_minutes / 60
    plan += f"## ⏰ Доступное время: ~{available_hours:.1f}ч\n\n"
    
    # Question
    plan += "❓ Что добавить/изменить в плане?\n"
    
    return plan


def main():
    """Main entry point"""
    # Load config
    config_path = Path(__file__).parent.parent / 'config.json'
    with open(config_path) as f:
        config = json.load(f)
    
    # Date
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Create daily file
    template_path = Path(__file__).parent.parent / config['obsidian']['template']
    diary_path = Path(config['obsidian']['vault_path']) / config['obsidian']['diary_path']
    diary_path.mkdir(parents=True, exist_ok=True)
    
    daily_file = create_daily_file(today, template_path, diary_path)
    
    # Get data
    events = get_calendar_events()
    tasks_data = get_tasks()
    
    # Format plan
    plan = format_plan(tasks_data, events)
    
    print(plan)


if __name__ == '__main__':
    main()
