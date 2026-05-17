#!/usr/bin/env python3
import sys
from collections import defaultdict

def main():
    current_date = None
    date_stats = defaultdict(lambda: {'pv': 0, 'uv': set()})
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            dt, user_id = line.split('\t', 1)
            date_stats[dt]['pv'] += 1
            date_stats[dt]['uv'].add(user_id)
        except:
            continue
    
    # 输出结果
    print("日期\t\tPV\tUV")
    print("-" * 40)
    for dt in sorted(date_stats.keys()):
        pv = date_stats[dt]['pv']
        uv = len(date_stats[dt]['uv'])
        print(f"{dt}\t{pv}\t{uv}")

if __name__ == "__main__":
    main()
