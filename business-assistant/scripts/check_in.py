#!/usr/bin/env python3
"""
Midday/afternoon check-in
"""

import sys

def main():
    time_of_day = sys.argv[1] if len(sys.argv) > 1 else "midday"
    
    if time_of_day == "midday":
        emoji = "🕐"
        time_label = "14:00"
    else:
        emoji = "🕔"
        time_label = "17:00"
    
    message = f"""{emoji} **Check-in ({time_label})**

Как идёт день?

✅ **Сделано:**
- (напиши что успел)

⏳ **В процессе:**
- (над чем работаешь)

🔄 **Нужно скорректировать план?**
"""
    
    print(message)


if __name__ == '__main__':
    main()
