
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
    
    male_21_30_average = 0.1*male_21_30_total 
    male_21_30_average = male_21_30_average + noise
    
    condition("male_21_30_average", 472_000)

    male_31_40_1 = Normal(mu=500_000, std=100)
    male_31_40_2 = Normal(mu=410_000, std=100)

    male_31_40_3 = Normal(mu=470_000, std=100)
    male_31_40_4 = Normal(mu=490_000, std=100)
    
    male_31_40_5 = Normal(mu=500_000, std=100)
    male_31_40_6 = Normal(mu=410_000, std=100)
    
    male_31_40_7 = Normal(mu=540_000, std=100)
    male_31_40_8 = Normal(mu=410_000, std=100)
    
    male_31_40_9 = Normal(mu=500_000, std=100)
    male_31_40_10 = Normal(mu=400_000, std=100)

    male_31_40_total = male_31_40_1 + male_31_40_2
    male_31_40_total = male_31_40_total + male_31_40_3
    male_31_40_total = male_31_40_total + male_31_40_4
    male_31_40_total = male_31_40_total + male_31_40_5
    male_31_40_total = male_31_40_total + male_31_40_6
    male_31_40_total = male_31_40_total + male_31_40_7
    male_31_40_total = male_31_40_total + male_31_40_8
    male_31_40_total = male_31_40_total + male_31_40_9
    male_31_40_total = male_31_40_total + male_31_40_10

    male_31_40_average = 0.1*male_31_40_total 
    
    condition("male_31_40_average", 516_000)

    male_41_50_1 = Normal(mu=580_000, std=100)
    male_41_50_2 = Normal(mu=530_000, std=100)
    
    male_41_50_3 = Normal(mu=590_000, std=100)
    male_41_50_4 = Normal(mu=510_000, std=100)

    male_41_50_5 = Normal(mu=560_000, std=100)
    male_41_50_6 = Normal(mu=590_000, std=100)
    
    male_41_50_7 = Normal(mu=280_000, std=100)
    male_41_50_8 = Normal(mu=500_000, std=100)
    
    male_41_50_9 = Normal(mu=580_000, std=100)
    male_41_50_10 = Normal(mu=600_000, std=100)
    
    male_41_50_total = male_41_50_1 + male_41_50_2
    male_41_50_total = male_41_50_total + male_41_50_3
    male_41_50_total = male_41_50_total + male_41_50_4
    male_41_50_total = male_41_50_total + male_41_50_5
    male_41_50_total = male_41_50_total + male_41_50_6
    male_41_50_total = male_41_50_total + male_41_50_7
    male_41_50_total = male_41_50_total + male_41_50_8
    male_41_50_total = male_41_50_total + male_41_50_9
    male_41_50_total = male_41_50_total + male_41_50_10

    male_41_50_average = 0.1*male_41_50_total 
    
    #condition("male_41_50_total", 570_000)

    male_51_60_1 = Normal(mu=680_000, std=100)
    male_51_60_2 = Normal(mu=570_000, std=100)

    male_51_60_3 = Normal(mu=620_000, std=100)
    male_51_60_4 = Normal(mu=610_000, std=100)

    male_51_60_5 = Normal(mu=600_000, std=100)
    male_51_60_6 = Normal(mu=570_000, std=100)

    male_51_60_7 = Normal(mu=700_000, std=100)
    male_51_60_8 = Normal(mu=600_000, std=100)
    
    male_51_60_9 = Normal(mu=520_000, std=100)
    male_51_60_10 = Normal(mu=770_000, std=100)

    male_51_60_total = male_51_60_1 + male_51_60_2
    male_51_60_total = male_51_60_total + male_51_60_3
    male_51_60_total = male_51_60_total + male_51_60_4
    male_51_60_total = male_51_60_total + male_51_60_5
    male_51_60_total = male_51_60_total + male_51_60_6
    male_51_60_total = male_51_60_total + male_51_60_7
    male_51_60_total = male_51_60_total + male_51_60_8
    male_51_60_total = male_51_60_total + male_51_60_9
    male_51_60_total = male_51_60_total + male_51_60_10

    male_51_60_average = 0.1*male_51_60_total 
    
    #condition("male_41_50_total", 678_000)

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
    
    female_21_30_average = 0.1*female_21_30_total 
    #condition("female_21_30_total", 425_000)
        
    total_21_30 = male_21_30_1 + male_21_30_2
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
    
    average_21_30 = 0.05 * total_21_30
    
    average_21_30 = average_21_30 + noise_1 
    
    condition("average_21_30", 448_500)
    
    total_male = male_21_30_1 + male_21_30_2
    total_male = total_male + male_21_30_3
    total_male = total_male + male_21_30_4
    total_male = total_male + male_21_30_5
    total_male = total_male + male_21_30_6
    total_male = total_male + male_21_30_7
    total_male = total_male + male_21_30_8
    total_male = total_male + male_21_30_9
    total_male = total_male + male_21_30_10
    
    total_male = total_male + male_31_40_1
    total_male = total_male + male_31_40_2
    total_male = total_male + male_31_40_3
    total_male = total_male + male_31_40_4
    total_male = total_male + male_31_40_5
    total_male = total_male + male_31_40_6
    total_male = total_male + male_31_40_7
    total_male = total_male + male_31_40_8
    total_male = total_male + male_31_40_9
    total_male = total_male + male_31_40_10
    
    total_male = total_male + male_41_50_1
    total_male = total_male + male_41_50_2
    total_male = total_male + male_41_50_3
    total_male = total_male + male_41_50_4
    total_male = total_male + male_41_50_5
    total_male = total_male + male_41_50_6
    total_male = total_male + male_41_50_7
    total_male = total_male + male_41_50_8
    total_male = total_male + male_41_50_9
    total_male = total_male + male_41_50_10

    
    total_male = total_male + male_51_60_1
    total_male = total_male + male_51_60_2
    total_male = total_male + male_51_60_3
    total_male = total_male + male_51_60_4
    total_male = total_male + male_51_60_5
    total_male = total_male + male_51_60_6
    total_male = total_male + male_51_60_7
    total_male = total_male + male_51_60_8
    total_male = total_male + male_51_60_9
    total_male = total_male + male_51_60_10
    
    average_male = 0.025* total_male 
    
    average_male = average_male + noise_2
    
    condition("average_male", 559_000)
    
    return male_21_30_1

