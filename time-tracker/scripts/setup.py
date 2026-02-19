#!/usr/bin/env python3
"""
Time Tracker Setup Script
Manages cron jobs for automatic time tracking
"""

import sys
import json
import argparse
from pathlib import Path

# Load config
SKILL_DIR = Path(__file__).parent.parent
CONFIG_PATH = SKILL_DIR / "config.json"

with open(CONFIG_PATH) as f:
    config = json.load(f)

# Job definitions
JOBS = {
    "tracking": {
        "name": "Time Tracking - каждые 30 минут",
        "schedule": {
            "kind": "cron",
            "expr": "*/30 8-22 * * *",  # Every 30 min, 8-22h
            "tz": config["tracking"]["timezone"]
        },
        "payload": {
            "kind": "agentTurn",
            "message": config["prompts"]["ask"] + " (time tracking)"
        },
        "sessionTarget": "isolated",
        "delivery": {
            "mode": "announce"
        },
        "enabled": True,
        "notify": False  # Not a user-facing reminder
    },
    "weekly": {
        "name": "Time Tracking - недельная сводка",
        "schedule": {
            "kind": "cron",
            "expr": "0 19 * * 5",  # Friday 19:00
            "tz": config["tracking"]["timezone"]
        },
        "payload": {
            "kind": "agentTurn",
            "message": config["prompts"]["weekly"]
        },
        "sessionTarget": "isolated",
        "delivery": {
            "mode": "announce"
        },
        "enabled": True,
        "notify": False
    }
}


def install():
    """Create cron jobs"""
    print("Installing Time Tracker cron jobs...\n")
    
    print("📋 Jobs to create:")
    for job_type, job_data in JOBS.items():
        print(f"\n  {job_type}:")
        print(f"    Name: {job_data['name']}")
        print(f"    Schedule: {job_data['schedule']['expr']} ({job_data['schedule']['tz']})")
        print(f"    Message: {job_data['payload']['message']}")
    
    print("\n" + "="*60)
    print("To install, run these commands via OpenClaw CLI:\n")
    
    for job_type, job_data in JOBS.items():
        job_json = json.dumps(job_data, ensure_ascii=False, indent=2)
        print(f"# {job_type.upper()}")
        print(f"openclaw cron add '{job_json}'\n")
    
    print("="*60)
    print("\nOr use the cron tool directly from agent session.")


def status():
    """Show current cron jobs"""
    print("To check status, run:")
    print("  openclaw cron list\n")
    print("Or ask agent: 'покажи активные cron jobs'")


def uninstall():
    """Remove cron jobs"""
    print("To uninstall, first get job IDs:")
    print("  openclaw cron list\n")
    print("Then remove:")
    print("  openclaw cron remove <job-id>\n")
    print("Or ask agent: 'удали time tracking cron jobs'")


def main():
    parser = argparse.ArgumentParser(description="Time Tracker Setup")
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
