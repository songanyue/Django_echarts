from scipy.special import comb, perm

from django.test import TestCase

# Create your tests here.
def ball(m, n):
    def C(a, b):
        def fraction(x):
            if x == 0:
                return 1
            return x * fraction(x - 1)
        if a < 0 or b < 0 or a < b:
            return print("错误！")
        return int((fraction(a) / fraction(b)) / fraction(a - b))
    return C(m - 1, n - 1)

def rename(name):
    nickname = name[0] + "某" * (len(name) - 1)
    return nickname

print(ball(4, 2))
print(rename("张三"))
print(rename("李小四"))
print(rename("赵老六儿"))