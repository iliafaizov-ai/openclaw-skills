#!/usr/bin/env python3
"""
Evening review - analyze day and prepare for tomorrow
"""

import json
from pathlib import Path
from datetime import datetime

def parse_daily_file(date_str: str, vault_path: str, diary_path: str):
    """Parse today's daily file for completed tasks"""
    daily_file = Path(vault_path) / diary_path / f"{date_str}.md"
    
    if not daily_file.exists():
        return {"completed": [], "incomplete": []}
    
    completed = []
    incomplete = []
    
    with open(daily_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith('- [x]') or line.strip().startswith('- [X]'):
                task = line.strip()[6:].strip()
                completed.append(task)
            elif line.strip().startswith('- [ ]'):
                task = line.strip()[6:].strip()
                incomplete.append(task)
    
    return {"completed": completed, "incomplete": incomplete}


def main():
    """Main entry point"""
    # Load config
    config_path = Path(__file__).parent.parent / 'config.json'
    with open(config_path) as f:
        config = json.load(f)
    
    # Parse today
    today = datetime.now().strftime('%Y-%m-%d')
    tasks = parse_daily_file(
        today,
        config['obsidian']['vault_path'],
        config['obsidian']['diary_path']
    )
    
    completed_count = len(tasks['completed'])
    incomplete_count = len(tasks['incomplete'])
    total = completed_count + incomplete_count
    
    completion_rate = (completed_count / total * 100) if total > 0 else 0
    
    # Format review
    review = f"""📊 **Итоги дня ({today})**

✅ **Сделано:** {completed_count}/{total} задач ({completion_rate:.0f}%)
"""
    
    if tasks['completed']:
        review += "\n**Выполнено:**\n"
        for task in tasks['completed'][:5]:
            review += f"- {task}\n"
    
    if tasks['incomplete']:
        review += f"\n⏳ **Не завершено:** {incomplete_count} задач(и)\n"
        review += "\n**Переносится на завтра:**\n"
        for task in tasks['incomplete'][:3]:
            review += f"- {task}\n"
    
    review += "\n💡 **Что помешало/помогло сегодня?**\n"
    review += "(Напиши свой инсайт — где время утекло, что сработало хорошо)\n\n"
    
    review += "📅 **Топ-3 приоритета на завтра:**\n"
    review += "1. \n2. \n3. \n"
    
    print(review)


if __name__ == '__main__':
    main()
