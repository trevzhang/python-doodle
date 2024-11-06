import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict
import random
import string


class FNVHash:
    @staticmethod
    def standard_fnv(key: str) -> int:
        FNV_PRIME = 0x01000193
        OFFSET_BASIS = 0x7ee36237

        hash_val = OFFSET_BASIS
        for c in key:
            hash_val ^= ord(c)
            hash_val *= FNV_PRIME
        return hash_val & 0x7FFFFFFF

    @staticmethod
    def non_prime_fnv(key: str) -> int:
        NON_PRIME = 0x01000190
        OFFSET_BASIS = 0x7ee36237

        hash_val = OFFSET_BASIS
        for c in key:
            hash_val ^= ord(c)
            hash_val *= NON_PRIME
        return hash_val & 0x7FFFFFFF


class HashAnalyzer:
    def __init__(self):
        self.test_data = []
        self.bucket_sizes = [100, 1000, 10000]

    def generate_test_data(self, size: int = 1000):
        # 生成随机字符串
        self.test_data = []
        for _ in range(size):
            length = random.randint(5, 15)
            self.test_data.append(''.join(random.choices(string.ascii_lowercase, k=length)))

        # 添加数字字符串
        for _ in range(size // 2):
            self.test_data.append(str(random.randint(0, 10000)))

        # 添加相似字符串
        for i in range(1, 11):
            self.test_data.append(f"user{i}")
            self.test_data.append(f"test{i}")

    def calculate_metrics(self, is_standard: bool, bucket_size: int) -> Dict:
        hash_func = FNVHash.standard_fnv if is_standard else FNVHash.non_prime_fnv
        distribution = {}
        unique_hashes = set()

        # 计算散列值分布
        for s in self.test_data:
            hash_val = hash_func(s) % bucket_size
            distribution[hash_val] = distribution.get(hash_val, 0) + 1
            unique_hashes.add(hash_val)

        # 计算指标
        collisions = [v - 1 for v in distribution.values() if v > 1]
        return {
            'coverage': len(unique_hashes) / bucket_size * 100,
            'avg_collisions': np.mean(collisions) if collisions else 0,
            'max_collisions': max(distribution.values()) - 1 if distribution else 0,
            'total_collisions': sum(collisions) if collisions else 0
        }

    def analyze_and_visualize(self):
        results = []
        for bucket_size in self.bucket_sizes:
            # 标准FNV
            standard_metrics = self.calculate_metrics(True, bucket_size)
            standard_metrics.update({'type': 'Standard FNV', 'bucket_size': bucket_size})
            results.append(standard_metrics)

            # 非素数FNV
            non_prime_metrics = self.calculate_metrics(False, bucket_size)
            non_prime_metrics.update({'type': 'Non-Prime FNV', 'bucket_size': bucket_size})
            results.append(non_prime_metrics)

        # 转换为DataFrame
        df = pd.DataFrame(results)

        # 创建可视化
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        # 添加主标题，包含数据集大小信息
        main_title = f'FNVHash Test (数据集大小: {len(self.test_data)})'
        fig.suptitle(main_title, fontsize=16, y=0.95)

        # 设置颜色
        colors = ['#4F81BD', '#C0504D']

        # 绘制四个指标的对比图
        metrics = [
            ('coverage', '覆盖率 (%)', axes[0, 0]),
            ('avg_collisions', '平均碰撞数', axes[0, 1]),
            ('max_collisions', '最大碰撞数', axes[1, 0]),
            ('total_collisions', '总碰撞数', axes[1, 1])
        ]

        bar_width = 0.35
        for metric, title, ax in metrics:
            # 获取数据
            standard_data = df[df['type'] == 'Standard FNV'][metric].values
            non_prime_data = df[df['type'] == 'Non-Prime FNV'][metric].values
            x = np.arange(len(self.bucket_sizes))

            # 绘制柱状图
            ax.bar(x - bar_width / 2, standard_data, bar_width, label='标准FNV', color=colors[0])
            ax.bar(x + bar_width / 2, non_prime_data, bar_width, label='非素数FNV', color=colors[1])

            # 设置图表属性
            ax.set_title(title)
            ax.set_xlabel('桶大小')
            ax.set_ylabel(title)
            ax.set_xticks(x)
            ax.set_xticklabels(self.bucket_sizes)
            ax.legend()

            # 添加数值标签
            for i, v in enumerate(standard_data):
                ax.text(i - bar_width / 2, v, f'{v:.1f}', ha='center', va='bottom')
            for i, v in enumerate(non_prime_data):
                ax.text(i + bar_width / 2, v, f'{v:.1f}', ha='center', va='bottom')

        plt.tight_layout()
        plt.show()

        # 打印详细统计数据
        print("\n详细统计数据:")
        pd.set_option('display.max_columns', None)
        print(df.round(2))


# 运行分析
if __name__ == "__main__":
    analyzer = HashAnalyzer()
    analyzer.generate_test_data(1000)
    analyzer.analyze_and_visualize()
