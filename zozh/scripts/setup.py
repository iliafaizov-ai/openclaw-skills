#!/usr/bin/env python3
"""
ЗОЖ Skill Setup Script
Manages cron jobs for nutrition and water tracking
"""

import sys
import json
from pathlib import Path

# Load config
SKILL_DIR = Path(__file__).parent.parent
CONFIG_PATH = SKILL_DIR / "config.json"

with open(CONFIG_PATH) as f:
    config = json.load(f)

# Job definitions
JOBS = {
    "meal_morning": {
        "name": "ЗОЖ - завтрак",
        "schedule": {
            "kind": "cron",
            "expr": "0 8 * * *",
            "tz": config["tracking"]["meals"]["timezone"]
        },
        "payload": {
            "kind": "agentTurn",
            "message": config["prompts"]["meal"] + " (завтрак)"
        },
        "sessionTarget": "isolated",
        "delivery": {"mode": "announce"},
        "enabled": True,
        "notify": False
    },
    "meal_lunch": {
        "name": "ЗОЖ - обед",
        "schedule": {
            "kind": "cron",
            "expr": "0 13 * * *",
            "tz": config["tracking"]["meals"]["timezone"]
        },
        "payload": {
            "kind": "agentTurn",
            "message": config["prompts"]["meal"] + " (обед)"
        },
        "sessionTarget": "isolated",
        "delivery": {"mode": "announce"},
        "enabled": True,
        "notify": False
    },
    "meal_dinner": {
        "name": "ЗОЖ - ужин",
        "schedule": {
            "kind": "cron",
            "expr": "0 17 * * *",
            "tz": config["tracking"]["meals"]["timezone"]
        },
        "payload": {
            "kind": "agentTurn",
            "message": config["prompts"]["meal"] + " (ужин)"
        },
        "sessionTarget": "isolated",
        "delivery": {"mode": "announce"},
        "enabled": True,
        "notify": False
    },
    "meal_evening": {
        "name": "ЗОЖ - вечерний приём",
        "schedule": {
            "kind": "cron",
            "expr": "0 21 * * *",
            "tz": config["tracking"]["meals"]["timezone"]
        },
        "payload": {
            "kind": "agentTurn",
            "message": config["prompts"]["meal"] + " (вечерний приём)"
        },
        "sessionTarget": "isolated",
        "delivery": {"mode": "announce"},
        "enabled": True,
        "notify": False
    },
    "water": {
        "name": "ЗОЖ - вода (каждый час)",
        "schedule": {
            "kind": "cron",
            "expr": f"0 {config['tracking']['water']['start_hour']}-{config['tracking']['water']['end_hour']} * * *",
            "tz": config["tracking"]["water"]["timezone"]
        },
        "payload": {
            "kind": "agentTurn",
            "message": config["prompts"]["water"]
        },
        "sessionTarget": "isolated",
        "delivery": {"mode": "announce"},
        "enabled": True,
        "notify": False
    },
    "daily_report": {
        "name": "ЗОЖ - дневная сводка",
        "schedule": {
            "kind": "cron",
            "expr": "0 23 * * *",
            "tz": config["tracking"]["meals"]["timezone"]
        },
        "payload": {
            "kind": "agentTurn",
            "message": config["prompts"]["daily_report"]
        },
        "sessionTarget": "isolated",
        "delivery": {"mode": "announce"},
        "enabled": config["reports"]["daily"]["enabled"],
        "notify": False
    },
    "weekly_report": {
        "name": "ЗОЖ - недельная сводка",
        "schedule": {
            "kind": "cron",
            "expr": "0 19 * * 0",  # Sunday 19:00
            "tz": config["tracking"]["meals"]["timezone"]
        },
        "payload": {
            "kind": "agentTurn",
            "message": config["prompts"]["weekly_report"]
        },
        "sessionTarget": "isolated",
        "delivery": {"mode": "announce"},
        "enabled": config["reports"]["weekly"]["enabled"],
        "notify": False
    }
}


def install():
    """Create cron jobs"""
    print("Installing ЗОЖ Skill cron jobs...\n")
    
    print("📋 Jobs to create:")
    for job_type, job_data in JOBS.items():
        status = "✅" if job_data["enabled"] else "⏸️"
        print(f"\n  {status} {job_type}:")
        print(f"    Name: {job_data['name']}")
        print(f"    Schedule: {job_data['schedule']['expr']} ({job_data['schedule']['tz']})")
        print(f"    Message: {job_data['payload']['message']}")
    
    print("\n" + "="*60)
    print("To install, run these commands via OpenClaw CLI or agent:\n")
    
    for job_type, job_data in JOBS.items():
        if not job_data["enabled"]:
            continue
        job_json = json.dumps(job_data, ensure_ascii=False, indent=2)
        print(f"# {job_type.upper()}")
        print(f"openclaw cron add '{job_json}'\n")
    
    print("="*60)
    print("\nOr use the cron tool directly from agent session.")


def status():
    """Show current cron jobs"""
    print("To check status, run:")
    print("  openclaw cron list\n")
    print("Or ask agent: 'покажи активные cron jobs для ЗОЖ'")


def uninstall():
    """Remove cron jobs"""
    print("To uninstall, first get job IDs:")
    print("  openclaw cron list | grep ЗОЖ\n")
    print("Then remove:")
    print("  openclaw cron remove <job-id>\n")
    print("Or ask agent: 'удали все ЗОЖ cron jobs'")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="ЗОЖ Skill Setup")
    parser.add_argument(
        "action",
        choices=["install", "status", "uninstall", "reinstall"],
        help="Action to perform"
    )
    
    args = parser.parse_args()
    
    if args.action == "install":
        install()
    elif args.action == "status":
        status()
    elif args.action == "uninstall":
        uninstall()
    elif args.action == "reinstall":
        uninstall()
        print("\n")
        install()


if __name__ == "__main__":
    main()
