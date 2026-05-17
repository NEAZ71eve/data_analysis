# 淘宝用户行为数据分析项目

基于淘宝用户行为数据集的大数据分析项目，支持多种技术方案部署。

## 项目概览

本项目使用淘宝用户行为数据集进行PV/UV分析，包含三种部署方案：

1. **Docker Compose + Hive** - 完整的大数据环境（推荐）
2. **Python + SQLite** - 轻量级快速分析
3. **Hadoop MapReduce** - 分布式计算方案

## 环境要求

- **方案一**: Docker & Docker Compose
- **方案二**: Python 3.8+ & pandas
- **方案三**: JDK 11 & Hadoop 3.3.6+

## 数据说明

- **数据集**: UserBehavior.csv（淘宝用户行为数据）
- **数据量**: 约1亿条记录
- **时间范围**: 2017-11-25 至 2017-12-03
- **字段**: user_id, item_id, category_id, behavior_type, timestamps

## 快速开始

### 方案二：Python + SQLite（快速上手）

```bash
# 安装依赖
pip install pandas

# 运行分析
python taobao_analysis.py
```

### 方案三：Hadoop MapReduce

```bash
# 配置环境（WSL 2）
source setup_hadoop_env.sh

# 运行分析
bash run_hadoop_analysis.sh
```

## 项目文件

| 文件 | 描述 |
|------|------|
| docker-compose.yml | Docker方案配置 |
| run_project.sh | Docker部署脚本 |
| taobao_analysis.py | Python分析脚本 |
| mapper.py | Hadoop Map阶段 |
| reducer.py | Hadoop Reduce阶段 |
| setup_hadoop_env.sh | 环境变量配置 |
| configure_hadoop_local.sh | Hadoop本地模式配置 |

## 分析结果示例

| 日期       | PV      | UV      |
|------------|---------|---------|
| 2017-11-25 | 93,932  | 6,782   |
| 2017-11-26 | 95,657  | 6,928   |
| 2017-12-02 | 123,514 | 9,271   |
| 2017-12-03 | 122,446 | 9,300   |

## 数据集说明

由于数据集较大（约2.2GB），未包含在仓库中，请从阿里云天池下载：

https://tianchi.aliyun.com/dataset/649

## License

MIT
