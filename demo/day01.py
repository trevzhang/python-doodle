x = 1
y = 2
for i in range(10):
    x, y = y, x + y
    print x, y
