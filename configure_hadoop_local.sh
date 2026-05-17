#!/bin/bash
# 配置Hadoop本地模式

source /mnt/d/s/BGDATA/setup_hadoop_env.sh

# 创建必要的目录
mkdir -p /tmp/hadoop/dfs/name
mkdir -p /tmp/hadoop/dfs/data
mkdir -p /tmp/hadoop/tmp

# 配置core-site.xml
cat > $HADOOP_CONF_DIR/core-site.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>file:///</value>
  </property>
  <property>
    <name>hadoop.tmp.dir</name>
    <value>/tmp/hadoop/tmp</value>
  </property>
</configuration>
EOF

# 配置hdfs-site.xml
cat > $HADOOP_CONF_DIR/hdfs-site.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>/tmp/hadoop/dfs/name</value>
  </property>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>/tmp/hadoop/dfs/data</value>
  </property>
</configuration>
EOF

# 配置mapred-site.xml
cat > $HADOOP_CONF_DIR/mapred-site.xml << 'EOF'
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>local</value>
  </property>
</configuration>
EOF

# 配置yarn-site.xml
cat > $HADOOP_CONF_DIR/yarn-site.xml << 'EOF'
<?xml version="1.0"?>
<configuration>
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
</configuration>
EOF

echo "✅ Hadoop本地模式配置完成"
