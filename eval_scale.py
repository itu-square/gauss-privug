

def f():
    male_21_30_1 = Normal(mu=1, std=1)
    sum_         = Normal(mu=0, std=0)
    for i in range(2500):
        sum_ = sum_ + male_21_30_1
    
    condition("2500", 0)
    return sum_
    