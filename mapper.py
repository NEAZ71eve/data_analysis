#!/usr/bin/env python3
import sys
from datetime import datetime

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split(',')
        if len(parts) < 5:
            continue
        try:
            user_id = parts[0]
            item_id = parts[1]
            category_id = parts[2]
            behavior_type = parts[3]
            timestamp = int(parts[4])
            
            # 过滤时间范围 2017-11-25 到 2017-12-03
            dt = datetime.fromtimestamp(timestamp)
            dt_str = dt.strftime('%Y-%m-%d')
            
            # 只统计PV行为
            if behavior_type == 'pv':
                print(f"{dt_str}\t{user_id}")
        except:
            continue

if __name__ == "__main__":
    main()
