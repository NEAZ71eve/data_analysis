import sqlite3
import pandas as pd
import os

CSV_PATH = r"-- UserBehavior.csv\UserBehavior.csv"
SAMPLE_ROWS = 1_000_000
DB_PATH = "taobao.db"

def extract_sample():
    if os.path.exists("sample.csv"):
        print("✅ sample.csv 已存在，跳过抽取")
        return
    print(f"📥 从 {CSV_PATH} 抽取前 {SAMPLE_ROWS} 行...")
    chunk = pd.read_csv(CSV_PATH, header=None, nrows=SAMPLE_ROWS,
                        names=['user_id','item_id','category_id','behavior_type','timestamps'])
    chunk.to_csv("sample.csv", index=False)
    print("✅ 采样完成")

def init_db_and_load():
    conn = sqlite3.connect(DB_PATH)
    print("🏗️ 创建表 ods_user_behavior...")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS ods_user_behavior (
            user_id INTEGER,
            item_id INTEGER,
            category_id INTEGER,
            behavior_type TEXT,
            timestamps INTEGER
        )
    ''')
    conn.execute("DELETE FROM ods_user_behavior")
    print("📤 导入数据...")
    df = pd.read_csv("sample.csv")
    df.to_sql("ods_user_behavior", conn, if_exists="append", index=False)
    conn.commit()

    print("🧹 创建 dwd_user_behavior...")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS dwd_user_behavior AS
        SELECT
            user_id,
            item_id,
            category_id,
            behavior_type,
            datetime(timestamps, 'unixepoch') AS event_time,
            date(timestamps, 'unixepoch') AS event_date,
            cast(strftime('%H', datetime(timestamps, 'unixepoch')) as int) AS event_hour
        FROM ods_user_behavior
        WHERE timestamps BETWEEN strftime('%s', '2017-11-25') AND strftime('%s', '2017-12-03')
          AND user_id IS NOT NULL
    ''')
    conn.commit()
    
    print("📊 创建 ads_daily_stats...")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS ads_daily_stats AS
        SELECT 
            event_date AS dt,
            COUNT(*) AS pv,
            COUNT(DISTINCT user_id) AS uv
        FROM dwd_user_behavior
        WHERE behavior_type = 'pv'
        GROUP BY event_date
        ORDER BY event_date
    ''')
    conn.commit()
    
    print("\n📋 每日 PV/UV 统计结果：")
    cursor = conn.execute("SELECT * FROM ads_daily_stats")
    rows = cursor.fetchall()
    print(f"{'日期':<12} {'PV':<10} {'UV':<10}")
    print("-" * 32)
    for row in rows:
        print(f"{row[0]:<12} {row[1]:<10} {row[2]:<10}")
    
    df_result = pd.read_sql("SELECT * FROM ads_daily_stats", conn)
    df_result.to_csv("result.csv", index=False)
    print("\n✅ 结果已导出到 result.csv")
    
    conn.close()

if __name__ == "__main__":
    if not os.path.exists(CSV_PATH):
        print(f"❌ 错误：未找到 {CSV_PATH}")
        print("请先下载 UserBehavior.csv 数据集放到当前目录")
        exit(1)
    
    extract_sample()
    init_db_and_load()