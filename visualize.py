import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 非交互式后端
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
def load_data():
    # 尝试从Hadoop结果文件读取
    try:
        df = pd.read_csv('result.csv')
        # 重命名列以保持一致性
        if 'dt' in df.columns:
            df = df.rename(columns={'dt': '日期', 'pv': 'PV', 'uv': 'UV'})
    except:
        # 创建示例数据
        data = {
            '日期': ['2017-11-25', '2017-11-26', '2017-11-27', '2017-11-28', 
                   '2017-11-29', '2017-11-30', '2017-12-01', '2017-12-02', '2017-12-03'],
            'PV': [93932, 95657, 87243, 88637, 91334, 94735, 98138, 123514, 122446],
            'UV': [6782, 6928, 6828, 6810, 6930, 7010, 7054, 9271, 9300]
        }
        df = pd.DataFrame(data)
    return df

def plot_trend(df):
    """绘制PV/UV趋势图"""
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # 转换日期格式
    df['日期'] = pd.to_datetime(df['日期'])
    
    # PV（左轴）
    color1 = 'tab:blue'
    ax1.set_xlabel('日期')
    ax1.set_ylabel('PV', color=color1)
    line1 = ax1.plot(df['日期'], df['PV'], color=color1, marker='o', linewidth=2, label='PV')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)
    
    # UV（右轴）
    ax2 = ax1.twinx()
    color2 = 'tab:orange'
    ax2.set_ylabel('UV', color=color2)
    line2 = ax2.plot(df['日期'], df['UV'], color=color2, marker='s', linewidth=2, label='UV')
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # 设置日期格式
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    
    # 添加图例
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')
    
    plt.title('淘宝用户行为 - 每日PV/UV趋势', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('pv_uv_trend.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✓ 趋势图已保存为: pv_uv_trend.png')

def plot_comparison(df):
    """绘制PV/UV对比图"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    df['日期'] = pd.to_datetime(df['日期'])
    
    # PV柱状图
    colors_pv = ['#1f77b4'] * len(df)
    max_pv_idx = df['PV'].idxmax()
    colors_pv[max_pv_idx] = '#ff7f0e'
    
    ax1.bar(df['日期'].dt.strftime('%Y-%m-%d'), df['PV'], color=colors_pv)
    ax1.set_title('每日PV统计', fontsize=12, fontweight='bold')
    ax1.set_ylabel('PV数量')
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.tick_params(axis='x', rotation=45)
    
    # UV柱状图
    colors_uv = ['#2ca02c'] * len(df)
    max_uv_idx = df['UV'].idxmax()
    colors_uv[max_uv_idx] = '#ff7f0e'
    
    ax2.bar(df['日期'].dt.strftime('%Y-%m-%d'), df['UV'], color=colors_uv)
    ax2.set_title('每日UV统计', fontsize=12, fontweight='bold')
    ax2.set_ylabel('UV数量')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('pv_uv_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✓ 对比图已保存为: pv_uv_comparison.png')

if __name__ == '__main__':
    print('=== 淘宝用户行为数据可视化 ===')
    df = load_data()
    
    print('\n数据预览:')
    print(df)
    
    print('\n生成图表...')
    plot_trend(df)
    plot_comparison(df)
    
    print('\n✅ 可视化完成！')
