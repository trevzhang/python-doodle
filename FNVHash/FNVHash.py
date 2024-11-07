import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random

class HashResult:
    def __init__(self):
        self.coverage = 0
        self.avg_collisions = 0
        self.max_collisions = 0
        self.total_collisions = 0
        self.distribution = {}

def standard_fnv(key):
    FNV_PRIME = 0x01000193
    OFFSET_BASIS = 0x7ee36237

    hash_value = OFFSET_BASIS
    for c in key:
        hash_value ^= ord(c)
        hash_value *= FNV_PRIME
    return hash_value & 0x7FFFFFFF

def non_prime_fnv(key):
    NON_PRIME = 0x01000190
    OFFSET_BASIS = 0x7ee36237

    hash_value = OFFSET_BASIS
    for c in key:
        hash_value ^= ord(c)
        hash_value *= NON_PRIME
    return hash_value & 0x7FFFFFFF

def calculate_metrics(test_data, is_standard, bucket_size):
    result = HashResult()
    unique_hashes = set()

    for s in test_data:
        hash_value = (standard_fnv(s) if is_standard else non_prime_fnv(s)) % bucket_size
        result.distribution[hash_value] = result.distribution.get(hash_value, 0) + 1
        unique_hashes.add(hash_value)

    result.max_collisions = max(result.distribution.values())
    result.total_collisions = sum(v - 1 for v in result.distribution.values() if v > 1)
    result.avg_collisions = result.total_collisions / len(result.distribution) if result.distribution else 0
    result.coverage = len(unique_hashes) / bucket_size * 100

    return result

def create_and_show_charts(test_data, bucket_sizes):
    coverage_data = []
    collisions_data = []
    max_collisions_data = []
    total_collisions_data = []

    for bucket_size in bucket_sizes:
        standard_result = calculate_metrics(test_data, True, bucket_size)
        non_prime_result = calculate_metrics(test_data, False, bucket_size)

        coverage_data.append({'Bucket Size': bucket_size, 'Hash Type': 'Standard FNV', 'Coverage': standard_result.coverage})
        coverage_data.append({'Bucket Size': bucket_size, 'Hash Type': 'Non-Prime FNV', 'Coverage': non_prime_result.coverage})

        collisions_data.append({'Bucket Size': bucket_size, 'Hash Type': 'Standard FNV', 'Avg Collisions': standard_result.avg_collisions})
        collisions_data.append({'Bucket Size': bucket_size, 'Hash Type': 'Non-Prime FNV', 'Avg Collisions': non_prime_result.avg_collisions})

        max_collisions_data.append({'Bucket Size': bucket_size, 'Hash Type': 'Standard FNV', 'Max Collisions': standard_result.max_collisions})
        max_collisions_data.append({'Bucket Size': bucket_size, 'Hash Type': 'Non-Prime FNV', 'Max Collisions': non_prime_result.max_collisions})

        total_collisions_data.append({'Bucket Size': bucket_size, 'Hash Type': 'Standard FNV', 'Total Collisions': standard_result.total_collisions})
        total_collisions_data.append({'Bucket Size': bucket_size, 'Hash Type': 'Non-Prime FNV', 'Total Collisions': non_prime_result.total_collisions})

    # 转换为 DataFrame
    coverage_df = pd.DataFrame(coverage_data)
    collisions_df = pd.DataFrame(collisions_data)
    max_collisions_df = pd.DataFrame(max_collisions_data)
    total_collisions_df = pd.DataFrame(total_collisions_data)

    # 创建图表
    plt.figure(figsize=(12, 10))

    plt.subplot(2, 2, 1)
    sns.barplot(data=coverage_df, x='Bucket Size', y='Coverage', hue='Hash Type')
    plt.title('Coverage (%)')

    plt.subplot(2, 2, 2)
    sns.barplot(data=collisions_df, x='Bucket Size', y='Avg Collisions', hue='Hash Type')
    plt.title('Average Collisions')

    plt.subplot(2, 2, 3)
    sns.barplot(data=max_collisions_df, x='Bucket Size', y='Max Collisions', hue='Hash Type')
    plt.title('Max Collisions')

    plt.subplot(2, 2, 4)
    sns.barplot(data=total_collisions_df, x='Bucket Size', y='Total Collisions', hue='Hash Type')
    plt.title('Total Collisions')

    plt.tight_layout()
    plt.show()

def main():
    # 生成测试数据
    test_data = []
    random.seed()

    # 生成1000个随机字符串
    for _ in range(1000):
        length = random.randint(5, 15)
        random_string = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(length))
        test_data.append(random_string)

    # 添加一些数字字符串和相似字符串
    for _ in range(500):
        test_data.append(str(random.randint(0, 9999)))

    for i in range(1, 11):
        test_data.append(f"user{i}")
        test_data.append(f"test{i}")

    # 测试不同桶大小
    bucket_sizes = [100, 1000, 10000]

    # 创建并显示图表
    create_and_show_charts(test_data, bucket_sizes)

if __name__ == "__main__":
    main()
