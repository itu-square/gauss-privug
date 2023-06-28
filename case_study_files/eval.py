


def f():
    male_21_30_1 = Normal(mu=480_000, std=100)
    male_21_30_2 = Normal(mu=490_000, std=100)
    
    male_21_30_3 = Normal(mu=440_000, std=100)
    male_21_30_4 = Normal(mu=420_000, std=100)
    
    male_21_30_5 = Normal(mu=490_000, std=100)
    male_21_30_6 = Normal(mu=490_000, std=100)
    
    male_21_30_7 = Normal(mu=520_000, std=100)
    male_21_30_8 = Normal(mu=490_000, std=100)
    
    male_21_30_9 = Normal(mu=470_000, std=100)
    male_21_30_10 = Normal(mu=400_000, std=100)
    
    male_21_30_total = male_21_30_1 + male_21_30_2
    male_21_30_total = male_21_30_total + male_21_30_3
    male_21_30_total = male_21_30_total + male_21_30_4
    male_21_30_total = male_21_30_total + male_21_30_5
    male_21_30_total = male_21_30_total + male_21_30_6
    male_21_30_total = male_21_30_total + male_21_30_7
    male_21_30_total = male_21_30_total + male_21_30_8
    male_21_30_total = male_21_30_total + male_21_30_9
    male_21_30_total = male_21_30_total + male_21_30_10
    
    male_21_30_total = male_21_30_total / 10
    
    condition("male_21_30_total", 472_000)
    return male_21_30_1

