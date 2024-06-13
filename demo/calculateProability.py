from math import comb

def calculate_probability(total_bets, total_prizes, my_bets):
    # 计算没有中奖的概率
    probability_no_win = comb(total_bets - total_prizes, my_bets) / comb(total_bets, my_bets)
    # 计算至少中一次奖的概率
    probability_at_least_one_win = 1 - probability_no_win
    return probability_at_least_one_win

# 我的押注次数
my_bets = 2
# 总押注次数
total_bets = 3980 + my_bets
# 奖品总数
total_prizes = 333

# 计算概率
probability = calculate_probability(total_bets, total_prizes, my_bets)
print(f"The probability of winning at least once is: {probability:.10f}")
