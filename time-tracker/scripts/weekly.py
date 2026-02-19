#!/usr/bin/env python3
"""
Weekly Time Tracking Report
Generates statistics and grouped activity report
"""

import re
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Paths
SKILL_DIR = Path(__file__).parent.parent
CONFIG_PATH = SKILL_DIR / "config.json"
CATEGORIES_PATH = SKILL_DIR / "references" / "categories.md"

with open(CONFIG_PATH) as f:
    config = json.load(f)

DIARY_PATH = Path.home() / ".openclaw" / "workspace" / config["storage"]["diary_path"]


def get_week_dates():
    """Get list of dates for current week (Mon-Sun)"""
    today = datetime.now()
    # Find Monday of current week
    monday = today - timedelta(days=today.weekday())
    return [monday + timedelta(days=i) for i in range(7)]


def parse_diary(date):
    """Parse time tracking entries from diary file"""
    diary_file = DIARY_PATH / f"{date.strftime('%Y-%m-%d')}.md"
    
    if not diary_file.exists():
        return []
    
    content = diary_file.read_text()
    entries = []
    
    # Find Time Tracking table
    in_tracking = False
    for line in content.split('\n'):
        if '## Time Tracking' in line:
            in_tracking = True
            continue
        
        if in_tracking:
            # Match table rows: | 08:00-08:30 | Activity |
            match = re.match(r'\|\s*(\d{2}:\d{2})-(\d{2}:\d{2})\s*\|\s*(.+?)\s*\|', line)
            if match:
                start, end, activity = match.groups()
                entries.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'start': start,
                    'end': end,
                    'activity': activity.strip(),
                    'duration_min': 30  # Fixed interval
                })
            elif line.startswith('##'):
                # Next section, stop parsing
                break
    
    return entries


def load_categories():
    """Load category keywords from categories.md"""
    if not CATEGORIES_PATH.exists():
        return {}
    
    content = CATEGORIES_PATH.read_text()
    categories = {}
    current_category = None
    current_subcategory = None
    
    for line in content.split('\n'):
        # Main category: ## 🏢 Работа
        if line.startswith('## '):
            current_category = re.sub(r'^##\s*[^\w\s]*\s*', '', line).strip()
            categories[current_category] = []
        
        # Subcategory: ### Программирование
        elif line.startswith('### '):
            current_subcategory = re.sub(r'^###\s*', '', line).strip()
        
        # Keywords: - Программирование
        elif line.startswith('- ') and current_category:
            keyword = line[2:].strip().lower()
            categories[current_category].append(keyword)
    
    return categories


def categorize_activity(activity, categories):
    """Assign category to activity based on keywords"""
    activity_lower = activity.lower()
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in activity_lower:
                return category
    
    return "Прочее"


def generate_report(entries, categories):
    """Generate grouped statistics"""
    if not entries:
        return "Нет данных за эту неделю."
    
    # Group by category
    by_category = defaultdict(lambda: {'count': 0, 'duration': 0, 'activities': []})
    
    for entry in entries:
        category = categorize_activity(entry['activity'], categories)
        by_category[category]['count'] += 1
        by_category[category]['duration'] += entry['duration_min']
        by_category[category]['activities'].append(entry['activity'])
    
    # Calculate totals
    total_duration = sum(cat['duration'] for cat in by_category.values())
    total_hours = total_duration / 60
    
    # Build report
    report = f"# 📊 Недельная сводка Time Tracking\n\n"
    report += f"**Всего отслежено:** {total_hours:.1f} часов ({len(entries)} записей)\n\n"
    report += f"## Распределение по категориям\n\n"
    
    # Sort by duration desc
    sorted_categories = sorted(
        by_category.items(),
        key=lambda x: x[1]['duration'],
        reverse=True
    )
    
    for category, data in sorted_categories:
        hours = data['duration'] / 60
        percentage = (data['duration'] / total_duration * 100) if total_duration > 0 else 0
        report += f"### {category}\n"
        report += f"- **Время:** {hours:.1f}ч ({percentage:.1f}%)\n"
        report += f"- **Записей:** {data['count']}\n"
        
        # Show top activities
        activity_counts = defaultdict(int)
        for act in data['activities']:
            activity_counts[act] += 1
        
        top_activities = sorted(
            activity_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        if top_activities:
            report += f"- **Топ активностей:**\n"
            for act, count in top_activities:
                report += f"  - {act} ({count}x)\n"
        
        report += "\n"
    
    return report


def main():
    """Generate weekly report"""
    print("Generating weekly time tracking report...\n")
    
    # Load categories
    categories = load_categories()
    print(f"Loaded {len(categories)} categories")
    
    # Get week dates
    week_dates = get_week_dates()
    print(f"Week: {week_dates[0].strftime('%Y-%m-%d')} - {week_dates[-1].strftime('%Y-%m-%d')}\n")
    
    # Parse all diaries
    all_entries = []
    for date in week_dates:
        entries = parse_diary(date)
        all_entries.extend(entries)
        if entries:
            print(f"  {date.strftime('%a %Y-%m-%d')}: {len(entries)} entries")
    
    print(f"\nTotal entries: {len(all_entries)}\n")
    
    # Generate report
    report = generate_report(all_entries, categories)
    print(report)
    
    # Save to file
    output_file = SKILL_DIR / f"weekly-report-{datetime.now().strftime('%Y-W%W')}.md"
    output_file.write_text(report)
    print(f"\n✅ Report saved: {output_file}")


if __name__ == "__main__":
    main()
