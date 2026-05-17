#!/bin/bash
# 使用Hadoop Streaming进行大数据分析

source /mnt/d/s/BGDATA/setup_hadoop_env.sh

# 设置输入和输出路径
INPUT_DIR="/tmp/user_behavior_input"
OUTPUT_DIR="/tmp/user_behavior_output"

# 清理旧数据
rm -rf $OUTPUT_DIR
mkdir -p $INPUT_DIR

# 复制数据到输入目录（使用已有的sample.csv）
cp /mnt/d/s/BGDATA/sample.csv $INPUT_DIR/

echo "🚀 开始Hadoop Streaming分析..."
echo "输入数据: $INPUT_DIR/sample.csv"

# 运行Hadoop Streaming作业
$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files /mnt/d/s/BGDATA/mapper.py,/mnt/d/s/BGDATA/reducer.py \
  -mapper /mnt/d/s/BGDATA/mapper.py \
  -reducer /mnt/d/s/BGDATA/reducer.py \
  -input $INPUT_DIR \
  -output $OUTPUT_DIR

echo ""
echo "✅ 分析完成！结果如下："
echo ""
$HADOOP_HOME/bin/hdfs dfs -cat $OUTPUT_DIR/part-00000 2>/dev/null || cat $OUTPUT_DIR/part-00000

echo ""
echo "📊 结果文件位置: $OUTPUT_DIR"
