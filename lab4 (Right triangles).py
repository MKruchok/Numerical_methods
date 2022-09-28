import math


# Group 33, variant 11
# Метод правих прямокутників
# ∫(1,2)x * sqrt(9 - x ** 2)

# Первісна
def F(x): return -(math.sqrt(9 - x ** 2) ** 3 / 3)


if __name__ == '__main__':
    a = 1
    b = 2
    n = 30
    integral = 0
    h = (b - a) / n
    x = a + h

    for i in range(n):
        integral += x * math.sqrt(9 - x ** 2)
        x += h
    integral *= h

    print("Відповідь:", integral)
    print("Перевірка F(b) - F(a):", F(b) - F(a))
