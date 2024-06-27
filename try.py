from random import Random

rnd_SociallyMotivated_bound = Random((1 + 5) * 17)
for _ in range(10):
    print(round( rnd_SociallyMotivated_bound.uniform(0.05, 0.5), 2))
