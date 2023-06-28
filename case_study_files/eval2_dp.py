


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
    
    noise = Normal(mu=0, std=1442533240)
    noise_1 = Normal(mu=0, std=1442533240)
    noise_2 = Normal(mu=0, std=1442533240)

    
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
    male_21_30_total = male_21_30_total + noise
    
    condition("male_21_30_total", 472_000)

    female_21_30_1 = Normal(mu=450_000, std=100)
    female_21_30_2 = Normal(mu=400_000, std=100)

    female_21_30_3 = Normal(mu=410_000, std=100)
    female_21_30_4 = Normal(mu=430_000, std=100)

    female_21_30_5 = Normal(mu=440_000, std=100)
    female_21_30_6 = Normal(mu=400_000, std=100)
    
    female_21_30_7 = Normal(mu=440_000, std=100)
    female_21_30_8 = Normal(mu=300_000, std=100)
    
    female_21_30_9 = Normal(mu=350_000, std=100)
    female_21_30_10 = Normal(mu=400_000, std=100)
    
    
    female_21_30_total = female_21_30_1 + female_21_30_2
    female_21_30_total = female_21_30_total + female_21_30_3
    female_21_30_total = female_21_30_total + female_21_30_4
    female_21_30_total = female_21_30_total + female_21_30_5
    female_21_30_total = female_21_30_total + female_21_30_6
    female_21_30_total = female_21_30_total + female_21_30_7
    female_21_30_total = female_21_30_total + female_21_30_8
    female_21_30_total = female_21_30_total + female_21_30_9
    female_21_30_total = female_21_30_total + female_21_30_10
    
    female_21_30_total = female_21_30_total / 10
    female_21_30_total = female_21_30_total + noise_1
 
    condition("female_21_30_total", 425_000)
    
    total_21_30   = Normal(mu=0, std=0)
    
    total_21_30 = total_21_30 + male_21_30_1
    total_21_30 = total_21_30 + male_21_30_2
    total_21_30 = total_21_30 + male_21_30_3
    total_21_30 = total_21_30 + male_21_30_4
    total_21_30 = total_21_30 + male_21_30_5
    total_21_30 = total_21_30 + male_21_30_6
    total_21_30 = total_21_30 + male_21_30_7
    total_21_30 = total_21_30 + male_21_30_8
    total_21_30 = total_21_30 + male_21_30_9
    total_21_30 = total_21_30 + male_21_30_10
    
    
    total_21_30 = total_21_30 + female_21_30_1
    total_21_30 = total_21_30 + female_21_30_2
    total_21_30 = total_21_30 + female_21_30_3
    total_21_30 = total_21_30 + female_21_30_4
    total_21_30 = total_21_30 + female_21_30_5
    total_21_30 = total_21_30 + female_21_30_6
    total_21_30 = total_21_30 + female_21_30_7
    total_21_30 = total_21_30 + female_21_30_8
    total_21_30 = total_21_30 + female_21_30_9
    total_21_30 = total_21_30 + female_21_30_10
    
    total_21_30 = total_21_30 / 20
    
    total_21_30 = total_21_30 + noise_2
    
    condition("total_21_30", 448_500)

    return male_21_30_1

    
   