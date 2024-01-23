import numpy as np
import matplotlib.pyplot as plt


# 定义函数
def custom_function(x):
    return -np.maximum(-5 * x - 7.7, 0) - np.maximum(-1.2 * x - 1.3, 0) - np.maximum(1.2 * x + 1, 0) + np.maximum(
        1.2 * x - 0.2, 0) + np.maximum(2 * x - 1.1, 0) + np.maximum(5 * x - 5, 0)


# 生成x值
x = np.linspace(-10, 10, 400)
# 计算对应的y值
y = custom_function(x)

# 绘制图像
plt.plot(x, y, label='ReLU')
plt.xlabel('x')
plt.ylabel('y')
plt.title('ReLU Graph')
plt.grid(True)
plt.legend()
plt.show()

