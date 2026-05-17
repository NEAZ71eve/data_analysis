#!/bin/bash
set -e

echo "🚀 启动 Hive 容器..."
docker compose up -d

echo "⏳ 等待 Hive 启动（约30秒）..."
sleep 30

echo "📥 下载淘宝数据集（约2.2GB）..."
wget -O UserBehavior.csv "https://tianchi.aliyun.com/dataset/649/download?spm=5176.12281978.0.0.3b9c4c2dX7pLkE" || curl -o UserBehavior.csv "https://tianchi.aliyun.com/dataset/649/download?spm=5176.12281978.0.0.3b9c4c2dX7pLkE"

echo "📤 将 CSV 复制到容器内..."
docker cp UserBehavior.csv hive:/tmp/

echo "🏗️ 创建 Hive 表并导入数据..."
docker exec -i hive beeline -u "jdbc:hive2://localhost:10000" -n root <<EOF
CREATE DATABASE IF NOT EXISTS taobao;
USE taobao;

CREATE TABLE ods_user_behavior (
    user_id BIGINT,
    item_id BIGINT,
    category_id BIGINT,
    behavior_type STRING,
    timestamps BIGINT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE;

LOAD DATA LOCAL INPATH '/tmp/UserBehavior.csv' OVERWRITE INTO TABLE ods_user_behavior;

CREATE TABLE dwd_user_behavior (
    user_id BIGINT,
    item_id BIGINT,
    category_id BIGINT,
    behavior_type STRING,
    event_time STRING,
    event_date STRING,
    event_hour INT
)
PARTITIONED BY (dt STRING);

SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

INSERT OVERWRITE TABLE dwd_user_behavior PARTITION(dt)
SELECT
    user_id,
    item_id,
    category_id,
    behavior_type,
    FROM_UNIXTIME(timestamps, 'yyyy-MM-dd HH:mm:ss') AS event_time,
    FROM_UNIXTIME(timestamps, 'yyyy-MM-dd') AS event_date,
    HOUR(FROM_UNIXTIME(timestamps)) AS event_hour,
    FROM_UNIXTIME(timestamps, 'yyyy-MM-dd') AS dt
FROM ods_user_behavior
WHERE timestamps BETWEEN UNIX_TIMESTAMP('2017-11-25') AND UNIX_TIMESTAMP('2017-12-03')
  AND user_id IS NOT NULL;

CREATE TABLE ads_daily_stats AS
SELECT 
    dt,
    COUNT(*) AS pv,
    COUNT(DISTINCT user_id) AS uv
FROM dwd_user_behavior
WHERE behavior_type = 'pv'
GROUP BY dt
ORDER BY dt;

SELECT * FROM ads_daily_stats LIMIT 20;
EOF

echo "✅ 分析完成！结果已保存在 Hive 表 ads_daily_stats 中。"
echo "💡 如需导出结果，执行：docker exec -i hive beeline -u jdbc:hive2://localhost:10000 --outputformat=csv2 -e 'SELECT * FROM taobao.ads_daily_stats;' > result.csv"