import numpy as np

mu, sigma = 0.6, 0.20

while True:
	s = np.random.normal(mu, sigma)
	print(s)